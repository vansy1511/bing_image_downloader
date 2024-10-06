import json

def get_quizzes_from_eval(eval_filepath):

    result = [{
        'word_to_image_description': [],
        'image_description_to_word': [],
    }]

    eval = json.load(open(eval_filepath, 'r', encoding='utf-8'))
    body_list = eval['body']

    for body in body_list:
        failed = []
        try:
            # Process for failed test-case
            split_text = body['outputs'][0]['text'].split("\n---\n")
            for noti in split_text[0].split("\n"):
                if noti.startswith("Failed"):
                    failed.append(noti.split()[2][:-1])
            output_quizzes = json.loads(split_text[1])['quizzes']
        except:
            # Process for passed test-case
            output_quizzes = json.loads(body['outputs'][0]['text'])['quizzes']

        for quiz in output_quizzes:
            if quiz['type'] == 'word_to_image_description':
                if quiz['type'] in failed:
                    quiz["pass"] = False
                else:
                    quiz["pass"] = True
                result[0]['word_to_image_description'].append(quiz)
            elif quiz['type'] == 'image_description_to_word':
                quiz['word'] = body['test']['vars']['word']
                if quiz['type'] in failed:
                    quiz["pass"] = False
                else:
                    quiz["pass"] = True
                result[0]['image_description_to_word'].append(quiz)
            else:
                continue

    return result

def main():
    eval_filepath = "eval_results/eval-2024-10-04T02_53_00-table.json"
    image_based_quizzes = get_quizzes_from_eval(eval_filepath)
    print(f"Number of `word_to_image_description` quizzes: {len(image_based_quizzes[0]['word_to_image_description'])}")
    print(f"Number of `image_description_to_word` quizzes: {len(image_based_quizzes[0]['image_description_to_word'])}")
    with open(f'image_based_quizzes/{eval_filepath.split("/")[-1].split(".")[0]}-image-based-quizzes.json', 'w') as f:
        json.dump(image_based_quizzes, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
