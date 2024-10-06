from pathlib import Path
import json
import re
from bing_image_downloader import downloader
import os
from tqdm import tqdm


def get_quiz_info(quiz_object: dict):
    query_list = []
    idx = 0

    quiz_type = quiz_object['type']
    quiz_choices = quiz_object['choices']

    if quiz_type == 'word_to_image_description':
        for choice in quiz_choices:
            query_string = choice['text']
            folder_string = "__".join([quiz_object['word'], str(quiz_object['pass']), quiz_type, query_string])
            folder = re.sub(r'[\\/*?:"<>|]', '', folder_string).replace(' ', '_')
            query_list.append({
                'idx': idx,
                'query_string': query_string,
                'folder': folder,
            })
            idx += 1

    if quiz_type == 'image_description_to_word':
        query_string = quiz_object['image_description']
        folder_string = "__".join([quiz_object['word'], str(quiz_object['pass']), quiz_type, query_string])
        folder = re.sub(r'[\\/*?:"<>|]', '', folder_string).replace(' ', '_')
        query_list.append({
            'idx': idx,
            'query_string': query_string,
            'folder': folder,
        })
        idx += 1


    return query_list



def download_images(folder, query_string, limit, filter):
    # check folder exists
    image_dir = Path('dataset').joinpath('filter', folder)
    if not os.path.exists(image_dir):        
        downloaded_image_pathds = downloader.download(
            query=query_string,
            limit=limit,
            output_dir=f"dataset/{filter}",
            sub_dir=folder,
            adult_filter_off=True,
            force_replace=True,
            filter=filter,
            timeout=60,
            verbose=True,
        )
        print(f"- Downloaded {len(downloaded_image_pathds)} images to {str(image_dir)}")
    else:
        print(f"- Folder '{folder}' already exists")
        # print(image_dir)
        pass

def main():
    final_results = []
    filter = 'custom_filter'
    with open('image_based_quizzes/eval-2024-10-04T02_53_00-table-image-based-quizzes.json', 'r') as f:
        image_based_quizzes = json.load(f)

    for quiz_object in image_based_quizzes[0]['word_to_image_description'][:5]:
        results = get_quiz_info(quiz_object)
        final_results.extend(results)
        for result in results:
            download_images(result['folder'], result['query_string'], 5, filter)
    
    for quiz_object in image_based_quizzes[0]['image_description_to_word']:
        results = get_quiz_info(quiz_object)
        final_results.extend(results)
        for result in results:
            download_images(result['folder'], result['query_string'], 5, filter)
    
    with open('image_based_qizzes/query_info.json', 'w') as f:
        f.write(json.dumps(final_results, indent=2, ensure_ascii=False))
    print("Downloaded images successfully")

if __name__ == '__main__':
    main()


# Debugging
# if __name__ == '__main__':
#     quiz_object = {
#         "id": 4,
#         "type": "image_description_to_word",
#         "image_description": "A group of people moving their bodies to the beat of music at a party.",
#         "choices": [
#           {
#             "correct": True,
#             "text": "dance"
#           },
#           {
#             "correct": False,
#             "text": "walk"
#           },
#           {
#             "correct": False,
#             "text": "read"
#           },
#           {
#             "correct": False,
#             "text": "cook"
#           }
#         ],
#         "word": "dance",
#         "pass": True
#       }
    
#     results = get_quiz_info(quiz_object)
#     with open('query_info.json', 'w') as f:
#         f.write(json.dumps(results, indent=2, ensure_ascii=False))
    
#     for result in results:
#         download_images(result['folder'], result['query_string'], 5, "custom_filter")