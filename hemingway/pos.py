"""Part of speech operations"""

import hemingway.data

def tokenize(text: str) -> list[str]:
    tokens = []
    
    first_pass = text.split(' ')
    
    for token in first_pass:
        for index, char in enumerate(token):
            if char in hemingway.data.punctuation:
                to_add = token[:index]
                tokens.append(to_add)
                tokens.append(token[index])
                token = token[index:]
        if token:
            tokens.append(token)

    return tokens

def tag_tokens(tokens: list[str]) -> list[tuple[str, str]]:
    first_pass = []

    for token in tokens:
        token = token.lower()
        if not token in hemingway.data.frequencies:
            lst = [token, ["?"]]
            first_pass.append(lst)
            continue
        probabilities = {}
        total = 0
        for pos in hemingway.data.frequencies[token]:
            total += float(hemingway.data.frequencies[token][pos])
            probabilities[pos] = float(hemingway.data.frequencies[token][pos]) / total
        lst = [token, probabilities]
        first_pass.append(lst)

    output = []
    completed = False
    probabilities = [item[1] for item in first_pass]

    while completed == False:
        collapsed = False
        for idx, probability in enumerate(probabilities):
            if len(probability.keys()) == 1:
                continue
            
            updated = check_rules(probability,tokens, idx, probabilities)
            if len(list(updated.keys())) == 1:
                collapsed = True
            for pos in updated:
                if updated[pos] == 1.0:
                    collapsed = True
            probabilities[idx] = updated
        if not collapsed:
            max_prob = 0
            collapse_idx = 0
            for idx, probability in enumerate(probabilities):
                if len(probability.keys()) == 1:
                    continue
                for pos in probability:
                    if probability[pos] > max_prob:
                        max_prob = probability[pos]
                        collapse_idx = idx
            for pos in probabilities[collapse_idx]:
                if probabilities[collapse_idx][pos] == max_prob:
                    probabilities[collapse_idx] = {pos: 1.0}
                    break
        all_collapsed = True
        for prob in probabilities:
            if len(prob.keys()) > 1:
                all_collapsed = False

        completed = all_collapsed
    
    for idx, token in enumerate(tokens):
        pos_list = probabilities[idx]
        pos_list = list(pos_list)
        output.append((token, pos_list[0]))

    return output

def check_rules(probability: dict, tokens: list, index: int, probabilities: list[dict]) -> dict:
    if "?" in probability:
        return {"?": 1.0}

    to_delete = []
    for pos in probability:
        pos_passed = False
        for rule in hemingway.data.rules[pos]:
            if "and" in rule:
                if process_and(rule["and"], tokens, index, probabilities):
                    pos_passed = True
                    break
            if "or" in rule:
                if process_or(rule["or"], tokens, index, probabilities):
                    pos_passed = True
                    break
            if "left" in rule:
                if process_left(rule, tokens, index, probabilities):
                    pos_passed = True
                    break
            if "right" in rule:
                if process_right(rule, tokens, index, probabilities):
                    pos_passed = True
                    break
            if "in" in rule:
                if process_in(rule, tokens, index):
                    pos_passed = True
                    break
        if len(hemingway.data.rules[pos]) == 0:
            pos_passed = True
        if not pos_passed:
            to_delete.append(pos)

    for key in to_delete:
        del probability[key]

    if len(probability) > 1:
        total = 0
        for pos in probability:
            total += probability[pos]
        for pos in probability:
            probability[pos] = probability[pos] / total
    elif len(probability) == 0:
        return {"?": 1.0}
    else:
        probability[list(probability.keys())[0]] = 1.0
    
    return probability

def process_and(rules: list[dict], tokens: list, index: int, probabilities: list[dict]) -> bool:
    bools = []
    for rule in rules:
        if "and" in rule:
            bools.append(process_and(rule["and"], tokens, index, probabilities))
        if "or" in rule:
            bools.append(process_or(rule["or"], tokens, index, probabilities))
        if "left" in rule:
            bools.append(process_left(rule, tokens, index, probabilities))
        if "right" in rule:
            bools.append(process_right(rule, tokens, index, probabilities))
        if "in" in rule:
            bools.append(process_in(rule, tokens, index))
    status = bools[0]
    for val in bools[1:]:
        status = status and val

    return status

def process_or(rules: list[dict], tokens: list, index: int, probabilities: list[dict]) -> bool:
    bools = []
    for rule in rules:
        if "and" in rule:
            bools.append(process_and(rule["and"], tokens, index, probabilities))
        if "or" in rule:
            bools.append(process_or(rule["or"], tokens, index, probabilities))
        if "left" in rule:
            bools.append(process_left(rule, tokens, index, probabilities))
        if "right" in rule:
            bools.append(process_right(rule, tokens, index, probabilities))
        if "in" in rule:
            bools.append(process_in(rule, tokens, index))
    status = bools[0]
    for val in bools[1:]:
        status = status or val

    return status

def process_left(rule: dict, tokens: list, index: int, probabilities: list[dict]) -> bool:
    parts = rule["left"]

    immediate = False
    if "immediate" in rule:
        immediate = rule["immediate"]
    
    is_not = False
    if "not" in rule:
        is_not = True

    found = False
    idx = index - 1
    while idx > 0:
        for pos in parts:
            if pos in probabilities[idx]:
                if probabilities[idx][pos] == 1.0:
                    found = True
        if immediate:
            break
        idx -= 1
    
    if is_not:
        return not found
    return found

def process_right(rule: dict, tokens: list, index: int, probabilities: list[dict]) -> bool:
    parts = rule["right"]

    immediate = False
    if "immediate" in rule:
        immediate = rule["immediate"]
    
    is_not = False
    if "not" in rule:
        is_not = True

    found = False
    idx = index + 1
    while idx < len(tokens):
        for pos in parts:
            if pos in probabilities[idx]:
                if probabilities[idx][pos] == 1.0:
                    found = True
        if immediate:
            break
        idx += 1
    
    if is_not:
        return not found
    return found

def process_in(rule: dict, tokens: list, index: int) -> bool:
    data_key = rule["in"]
    data_obj = hemingway.data.data[data_key]

    is_not = False
    if "not" in rule:
        is_not = True

    for to_check in data_obj:
        if check_token(tokens, index, to_check):
            return not is_not
        
    return is_not

def check_token(tokens: list, index: int, to_check: list) -> bool:
    if len(to_check) == 1:
        return tokens[index] == to_check[0]
    if len(to_check) == 2:
        if index > 1:
            if tokens[index - 1] == to_check[0] and tokens[index] == to_check[1]:
                return True
        if index < len(tokens) - 1:
            if tokens[index] == to_check[0] and tokens[index + 1] == to_check[1]:
                return True
        return False
    if index > 2:
        if tokens[index - 2] == to_check[0] and tokens[index - 1] == to_check[1] and tokens[index] == to_check[2]:
            return True
    if index > 1 and index < len(tokens) - 1:
        if tokens[index - 1] == to_check[0] and tokens[index] == to_check[1] and tokens[index + 1] == to_check[2]:
            return True
    if index < len(tokens) - 2:
        if tokens[index] == to_check[0] and tokens[index + 1] == to_check[1] and tokens[index + 2] == to_check[2]:
            return True
    return False

    
