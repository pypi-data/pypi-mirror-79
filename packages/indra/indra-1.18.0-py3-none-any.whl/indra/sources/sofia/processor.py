import itertools
from indra.statements import Influence, Concept, Event, Evidence, \
    WorldContext, TimeContext, RefContext, QualitativeDelta


pos_rels = ['provide', 'led', 'lead', 'driv', 'support', 'enabl', 'develop',
            'increas', 'ris']
neg_rels = ['restrict', 'worsen', 'declin', 'limit', 'constrain',
            'decreas', 'hinder', 'deplet', 'reduce', 'hamper']
neu_rels = ['affect', 'impact', 'due', 'caus', 'because']


class SofiaProcessor(object):
    @staticmethod
    def process_event(event_dict):
        mappings = [
            ('Event_Type', 'Event_Type'),
            ('Relation', 'Relation'),
            ('Location', 'Location'),
            ('Time', 'Time'),
            ('Source', 'Source_File'),
            ('Text', 'Sentence'),
            ('Agent_index', 'Agent Index'),
            ('Patient_index', 'Patient Index'),
            ('Agent', 'Agent'),
            ('Patient', 'Patient'),
            ('Event Index', 'Event Index')
        ]
        return {k: event_dict.get(v) for k, v in mappings}

    def _build_influences(self, rel_dict):
        stmt_list = []
        cause_entries = rel_dict.get('Cause Index')
        effect_entries = rel_dict.get('Effect Index')

        # FIXME: Handle cases in which there is a missing cause/effect
        if not cause_entries or not effect_entries:
            return []
        causes = [c.strip() for c in cause_entries.split(', ')]
        effects = [e.strip() for e in effect_entries.split(', ')]
        rel = rel_dict.get('Relation')
        if _in_rels(rel, pos_rels):
            pol = 1
        elif _in_rels(rel, neg_rels):
            pol = -1
        elif _in_rels(rel, neu_rels):
            pol = None
        # If we don't recognize this relation, we don't get any
        # statements
        else:
            return []

        text = rel_dict.get('Sentence')
        annot_keys = ['Relation']
        annots = {k: rel_dict.get(k) for k in annot_keys}
        ref = rel_dict.get('Source_File')

        for cause_idx, effect_idx in itertools.product(causes, effects):
            cause = self._events.get(cause_idx)
            effect = self._events.get(effect_idx)
            if not cause or not effect:
                continue
            subj = self.get_event(cause)
            obj = self.get_event(effect)

            ev = Evidence(source_api='sofia', pmid=ref,
                          annotations=annots, text=text)
            stmt = Influence(subj, obj, evidence=[ev])
            # Use the polarity of the events, if object does not have a
            # polarity, use overall polarity
            if stmt.obj.delta.polarity is None:
                stmt.obj.delta.set_polarity(pol)

            stmt_list.append(stmt)
        return stmt_list

    @staticmethod
    def get_event(event_entry):
        name = event_entry['Relation']
        concept = Concept(name, db_refs={'TEXT': name})
        grounding = event_entry['Event_Type']
        if grounding:
            concept.db_refs['SOFIA'] = grounding
        context = WorldContext()
        time = event_entry.get('Time')
        if time:
            context.time = TimeContext(text=time.strip())
        loc = event_entry.get('Location')
        if loc:
            context.geo_location = RefContext(name=loc)

        text = event_entry.get('Text')
        ref = event_entry.get('Source')
        agent = event_entry.get('Agent')
        patient = event_entry.get('Patient')
        anns = {}
        if agent:
            anns['agent'] = agent
        if patient:
            anns['patient'] = patient
        ev = Evidence(source_api='sofia', pmid=ref, text=text,
                      annotations=anns, source_id=event_entry['Event Index'])
        pol = event_entry.get('Polarity')
        event = Event(concept, context=context, evidence=[ev],
                      delta=QualitativeDelta(polarity=pol, adjectives=None))

        return event

    def get_relation_events(self, rel_dict):
        # Save indexes of events that are part of causal relations
        relation_events = []
        cause_entries = rel_dict.get('Cause Index')
        effect_entries = rel_dict.get('Effect Index')
        causes = [c.strip() for c in cause_entries.split(',')]
        effects = [e.strip() for e in effect_entries.split(',')]
        for ci in causes:
            relation_events.append(ci)
        for ei in effects:
            relation_events.append(ei)
        return relation_events

    def get_meaningful_events(self, raw_event_dict):
        # Only keep meaningful events and extract polarity information from
        # events showing change
        processed_event_dict = {}
        for event_index, event_info in raw_event_dict.items():
            ai = event_info['Agent_index']
            agent_index = [] if not ai else ai.split(', ')
            pi = event_info['Patient_index']
            patient_index = [] if not pi else pi.split(', ')

            if _in_rels(event_info['Relation'], pos_rels):
                pol = 1
            elif _in_rels(event_info['Relation'], neg_rels):
                pol = -1
            else:
                pol = None

            agent_embedded_events = agent_index and \
                all(a in raw_event_dict for a in agent_index)
            patient_embedded_events = patient_index and \
                all(a in raw_event_dict for a in patient_index)
            # If the agent is itself an event, we use that as the reference
            if agent_embedded_events:
                for event_ix in agent_index:
                    processed_event_dict[event_ix] = raw_event_dict[event_ix]
                    processed_event_dict[event_ix]['Polarity'] = pol
            # If the patient is itself an event, we use that as the reference
            elif patient_embedded_events:
                for event_ix in patient_index:
                    processed_event_dict[event_ix] = raw_event_dict[event_ix]
                    processed_event_dict[event_ix]['Polarity'] = pol
            # Otherwise we take the event itself
            else:
                processed_event_dict[event_index] = raw_event_dict[event_index]
        return processed_event_dict


class SofiaJsonProcessor(SofiaProcessor):
    def __init__(self, jd):
        self._events = self.process_events(jd)
        self.statements = []
        self.relation_subj_obj_ids = []

    def process_events(self, jd):
        event_dict = {}
        # First get all events from reader output
        events = jd['events']
        for event in events:
            event_index = event.get('Event Index')
            event_dict[event_index] = self.process_event(event)
        processed_event_dict = self.get_meaningful_events(event_dict)
        return processed_event_dict

    def extract_relations(self, jd):
        stmts = []
        for rel_dict in jd['causal']:
            # Save indexes of causes and effects
            current_relation_events = self.get_relation_events(rel_dict)
            for ix in current_relation_events:
                self.relation_subj_obj_ids.append(ix)
            # Make Influence Statements
            stmt_list = self._build_influences(rel_dict)
            if not stmt_list:
                continue
            stmts = stmts + stmt_list
        for stmt in stmts:
            self.statements.append(stmt)

    def extract_events(self, json_list):
        # First confirm we have extracted event information and relation events
        if not self._events:
            self.process_events(json_list)
        if not self.relation_subj_obj_ids:
            self.extract_relations(json_list)
        # Only make Event Statements from standalone events
        for event_index in self._events:
            if event_index not in self.relation_subj_obj_ids:
                event = self.get_event(self._events[event_index])
                self.statements.append(event)


class SofiaExcelProcessor(SofiaProcessor):
    def __init__(self, relation_rows, event_rows, entity_rows):
        self._events = self.process_events(event_rows)
        self.statements = []
        self.relation_subj_obj_ids = []

    def process_events(self, event_rows):
        header = [cell.value for cell in next(event_rows)]
        event_dict = {}
        for row in event_rows:
            row_values = [r.value for r in row]
            row_dict = {h: v for h, v in zip(header, row_values)}
            event_index = row_dict.get('Event Index')
            event_dict[event_index] = self.process_event(row_dict)
        processed_event_dict = self.get_meaningful_events(event_dict)
        return processed_event_dict

    def extract_relations(self, relation_rows):
        header = [cell.value for cell in next(relation_rows)]
        stmts = []
        for row in relation_rows:
            row_values = [r.value for r in row]
            row_dict = {h: v for h, v in zip(header, row_values)}
            # Save indexes of causes and effects
            current_relation_events = self.get_relation_events(row_dict)
            for ix in current_relation_events:
                self.relation_subj_obj_ids.append(ix)
            # Make Influence Statements
            stmt_list = self._build_influences(row_dict)
            if not stmt_list:
                continue
            stmts = stmts + stmt_list
        for stmt in stmts:
            self.statements.append(stmt)

    def extract_events(self, event_rows, relation_rows):
        # First confirm we have extracted event information and relation events
        if not self._events:
            self.process_events(event_rows)
        if not self.relation_subj_obj_ids:
            self.extract_relations(relation_rows)
        # Only make Event Statements from standalone events
        for event_index in self._events:
            if event_index not in self.relation_subj_obj_ids:
                event = self.get_event(self._events[event_index])
                self.statements.append(event)


def _in_rels(value, rels):
    for rel in rels:
        if value is not None:
            if value.lower().startswith(rel):
                return True
            if rel in value.lower():
                return True
    return False
