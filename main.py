from src import call_me_maybe
import json

if __name__ == '__main__':
    import time
    start = time.time()
    # print(call_me_maybe("great Shrek"))
    with open("data/input/function_calling_tests.json", "r") as test_file:
        # data = json.load(test_file)
        data = json.loads(test_file.read())

    final_dict = []
    for i in data:
        x = call_me_maybe(i['prompt'])
        print(x)
        print(f"\ntook {time.time() - start}\n\n")
        final_dict.append(x)

    print(final_dict)
    print(f"\ntotal {time.time() - start}\n\n")
