from collections import defaultdict


class TooLongInputError(ValueError):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


def check_and_apply(mask, match, identity):
    conflicts = []
    start = match[0]
    position = start
    while position <= match[1]:
        if mask[position] is not None:
            conflicts.append(mask[position])
        mask[position] = identity
        position += 1
    return list(set(conflicts))


def check_all_apply(projection, match, match_id):
    conflicts = []
    start = match[0]
    position = start
    while position <= match[1]:
        if len(projection[position]) > 0:
            conflicts.extend(projection[position])
        projection[position].append(match_id)
        position += 1
    return list(set(conflicts))


def transform_projection(matches, projection):
    bounds = [None] * len(matches)
    order = [None] * len(matches)

    match_num = 0
    for i, item in enumerate(projection):
        for j in item:
            if not bounds[j]:
                order[match_num] = j
                bounds[j] = (i,)
                match_num += 1
            else:
                bounds[j] = (bounds[j][0], i)
    for index in order:
        if len(bounds[index]) == 1:
            bounds[index] = (bounds[index][0], bounds[index][0])
        yield (index, (bounds[index]))


def discover_tree(ordered):
    tree = defaultdict(dict)

    anchor = (-2, 0)
    # ((node_id, tree_banch[node], index), (start_position, end_position))
    root = ((-1, tree[anchor], 0), (0, -1))

    stack = [root]
    while len(stack) > 0:
        ancestors = stack
        stack = []
        for item in ancestors:
            node_id, parent_branch, index = item[0]
            node_pos = item[1]

            weight = node_pos[1] - node_pos[0] + 1
            parent_branch[(node_id, weight)] = {}

            branch = parent_branch[(node_id, weight)]

            children = find_children(branch, node_pos, index, ordered)
            stack.extend(children)
    return tree[anchor]


def find_children(branch, parent_pos, index, ordered):
    children = []
    for i, item in enumerate(ordered[index:]):
        _id, _pos = item
        if _pos[0] > parent_pos[1]:
            if len(children) > 0 and _pos[0] > children[0][1][1]:
                break
            children.append(((_id, branch, i + index), _pos))
    return children


def traverse_tree(tree, node=None, path=[], weight=0):
    if node:
        path.append(node[0])
        weight += node[1]
    if len(tree) == 0:
        yield path[1:], weight

    for k, v in tree.items():
        yield from traverse_tree(v, k, path[:], weight)


def find_best_path(tree):
    max_weight = 0
    best = []
    for i, item in enumerate(traverse_tree(tree)):
        sequence = item[0]
        weight = item[1]
        if weight > max_weight:
            max_weight = weight
            best = sequence
    return best


class RuleMatcher:

    def __init__(self):
        self._reset()

    def _reset(self):
        self._matches = []
        self._state = 'None'
        self._start = None
        self._previous_symbol = None
        self._rule_position = 0

    def match(self, sequence, rule):
        self._sequence = sequence
        self._rule = rule
        self._reset()

        for i, ch in enumerate(self._sequence):
            if self._state == 'None':
                self._on_none_state(i, ch)
            elif self._state == 'ClosedRule':
                self._on_closed_state(i, ch)
            elif self._state == 'OpenRule':
                self._on_open_state(i, ch)
            self._previous_symbol = ch

        return self._matches

    def _on_none_state(self, i, ch):
        if ch == self._rule[0]:
            if len(self._rule) == 1:
                self._state = 'ClosedRule'
                if i + 1 == len(self._sequence):
                    self._matches.append((i, i))
                    self._state = 'None'
                    self._rule_position = 0
                    self._start = None
            else:
                self._state = 'OpenRule'
            self._start = i

    def _on_closed_state(self, i, ch):
        if self._previous_symbol != ch:
            self._matches.append((self._start, i - 1))
            self._state = 'None'
            self._rule_position = 0
            self._start = None
        elif i + 1 == len(self._sequence):
            if ch == self._rule[self._rule_position]:
                self._matches.append((self._start, i))
            else:
                self._matches.append((self._start, i - 1))
            self._state = 'None'
            self._rule_position = 0
            self._start = None

    def _on_open_state(self, i, ch):
        if ch != self._previous_symbol:
            if (len(self._rule) == self._rule_position + 1 or
                    i + 1 == len(self._sequence)):
                self._state = 'ClosedRule'
                if (ch != self._rule[self._rule_position] and
                        self._rule_position > 0):
                    if i + 1 == len(self._sequence):
                        self._matches.append((self._start, i))
                    else:
                        self._matches.append((self._start, i - 1))
                    self._state = 'None'
                    self._rule_position = 0
                    self._start = None
                elif (i + 1 == len(self._sequence) and
                      ch == self._rule[len(self._rule) - 1]):
                    self._matches.append((self._start, i))
                    self._state = 'None'
                    self._rule_position = 0
                    self._start = None
            else:
                if ch == self._rule[self._rule_position + 1]:
                    if (ch == self._rule[len(self._rule) - 1] and
                            (i + 1 == len(self._sequence) or
                             self._sequence[i + 1] != ch) and
                            self._rule_position + 1 == len(self._rule) - 1):

                        self._matches.append((self._start, i))
                        self._state = 'None'
                        self._rule_position = 0
                        self._start = None
                    else:
                        self._rule_position += 1
                else:
                    self._state = 'None'
        else:
            if (ch == self._rule[len(self._rule) - 1] and
                    (i + 1 == len(self._sequence) or
                     self._sequence[i + 1] != ch) and
                    self._rule_position > 0):
                self._matches.append((self._start, i))
                self._state = 'None'
                self._rule_position = 0
                self._start = None


def find_matches(sequence, grammar, overlaps=False, allowed_length=120):
    if len(sequence) > allowed_length:
        raise TooLongInputError('Input is expected to be relatively short. For now'
                                'its length set to be equal {}'.format(allowed_length))

    matches = {
        'matches': [],
        'rules': [],
    }
    projection = [[] for item in range(len(sequence))]

    rule_matcher = RuleMatcher()

    for rule in grammar:
        matched = rule_matcher.match(sequence, rule)
        matches['matches'] += matched
        matches['rules'] += [rule] * len(matched)

    results = {
        'matches': [],
        'rules': [],
    }
    if overlaps:
        results = matches
    else:
        for _id, match in enumerate(matches['matches']):
            check_all_apply(projection, match, _id)

        ordered_data = list(
            transform_projection(matches['matches'], projection))
        tree = discover_tree(ordered_data)

        for i in find_best_path(tree):
            results['matches'].append(matches['matches'][i])
            results['rules'].append(matches['rules'][i])

    return results
