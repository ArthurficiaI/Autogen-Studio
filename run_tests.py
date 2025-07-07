import custom_tools
#docker run -p 8082:8080   -v "/mnt/c/Users/dafwe/OneDrive/Desktop/Unistuff/Master/2. Semester/Automated Software Engineering/Frameworks/AutogenStudio/repos:/repos"   -v /var/run/docker.sock:/var/run/docker.sock   paulroewer/swe-bench-lite-tester


import os, requests,json
LOG_FILE = "results.log"

def call_tests(testcase_index : int) -> str:
    root_root_dir = os.getcwd()
    root_dir = os.path.join(os.getcwd(),r"repos")
    repo_dir = os.path.join(root_dir, f"repo_{testcase_index}")

    print(repo_dir)


    try:
        response = requests.get(f"http://localhost:8081/task/index/{testcase_index}")
        print(response)
        if response.status_code != 200:
            raise Exception(f"Invalid response: {response.status_code}")

        testcase = response.json()
        prompt = testcase["Problem_statement"]
        git_clone = testcase["git_clone"]
        fail_tests = json.loads(testcase.get("FAIL_TO_PASS", "[]"))
        pass_tests = json.loads(testcase.get("PASS_TO_PASS", "[]"))
        instance_id = testcase["instance_id"]


        test_payload = {
            "instance_id": instance_id,
            "repoDir": f"/repos/repo_{testcase_index}",  # mount with docker
            "FAIL_TO_PASS": fail_tests,
            "PASS_TO_PASS": pass_tests
        }
        res = requests.post("http://localhost:8082/test", json=test_payload)
        res.raise_for_status()
        result_raw = res.json().get("harnessOutput", "{}")
        result_json = json.loads(result_raw)
        if not result_json:
            return "No data in harnessOutput – possible evaluation error or empty result"
        instance_id = next(iter(result_json))
        tests_status = result_json[instance_id]["tests_status"]
        fail_pass_results = tests_status["FAIL_TO_PASS"]
        fail_pass_total = len(fail_pass_results["success"]) + len(fail_pass_results["failure"])
        fail_pass_passed = len(fail_pass_results["success"])
        pass_pass_results = tests_status["PASS_TO_PASS"]
        pass_pass_total = len(pass_pass_results["success"]) + len(pass_pass_results["failure"])
        pass_pass_passed = len(pass_pass_results["success"])

        # Log results
        return_string = ""

        os.chdir(root_root_dir)
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"\n--- TESTCASE {testcase_index} ---\n")
            log.write(f"FAIL_TO_PASS passed: {fail_pass_passed}/{fail_pass_total}\n")
            log.write(f"PASS_TO_PASS passed: {pass_pass_passed}/{pass_pass_total}\n")
            return f"\n--- TESTCASE {testcase_index} ---\n" + f"FAIL_TO_PASS passed: {fail_pass_passed}/{fail_pass_total}\n" + f"PASS_TO_PASS passed: {pass_pass_passed}/{pass_pass_total}\n"
    except Exception as e:
        os.chdir(root_root_dir)
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"\n--- TESTCASE {testcase_index} ---\n")
            log.write(f"Error: {e}\n")
            print(f"Error in test case{testcase_index}: {e}")


for i in range(9, 11):
    print(call_tests(i))

def get_all_prompts():

    for i in (0,100):
        try:
            response = requests.get(f"http://localhost:8081/task/index/{i}")
            print(response)
            if response.status_code != 200:
                raise Exception(f"Invalid response: {response.status_code}")

            testcase = response.json()
            prompt = testcase["Problem_statement"]

            with open("prompts.txt", "a",encoding="utf-8") as prompts:
                prompts.write(f"Testcase {i}:\n")
                prompts.write(f"{prompt}\n\n\n")

        except Exception:
            print("Error")


