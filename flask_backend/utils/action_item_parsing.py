from evaluate import load
bertscore = load("bertscore")

# Setting use_fast_tokenizer to true can speed up the process about 5X
def bertscore_calc(predictions, references):
    results = bertscore.compute(predictions=predictions, references=references, lang="en", use_fast_tokenizer = True)
    return results['f1']

'''
Input: 2d list, each sublist contains action items extracted from a small chunk of transcript.
Output: 2d list, where each sublist has removed overlapping action items with the previous chunk.
'''
def action_item_processing(lists):
    ret = [lists[0]]
    for i in range (1, len(lists)):
        prev = lists[i-1]
        cur = lists[i]
        newcur = []
        
        for action_item in cur:
            flag = True
            target = [action_item] * len(prev)
            score = bertscore_calc(target, prev)
            for s in score:
                if s > 0.93:
                    flag = False
                    break
            if flag:
                newcur.append(action_item)
            else:
                print("Utils: " + action_item + " was removed for duplicate.")
        if len(newcur) > 0:
            ret.append(newcur)

    return ret
            