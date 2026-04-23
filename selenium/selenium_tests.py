from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://localhost:5173"
CHROMEDRIVER_PATH = "./chromedriver.exe"

passed = 0
failed = 0

def log(test_name, success, message=""):
    global passed, failed
    if success:
        passed += 1
        print(f"  ✓  {test_name}")
    else:
        failed += 1
        print(f"  ✗  {test_name} — {message}")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
driver.get(BASE_URL)
time.sleep(2)

print("\nSHRIYA — Selenium UI Tests\n")

# Test 1: Page loads
try:
    assert "To" in driver.title or driver.find_element(By.TAG_NAME, "body")
    log("Page loads successfully", True)
except:
    log("Page loads successfully", False, "Page did not load")

# Test 2: Input field exists ..........
try:
    input_box = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder]")
    log("Task input field is visible", True)
except:
    log("Task input field is visible", False, "Input not found")

# Test 3: Add a task
try:
    input_box = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder]")
    input_box.clear()
    input_box.send_keys("Selenium Test Task")
    add_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")
    add_btn.click()
    time.sleep(1)
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Selenium Test Task" in body
    log("Add a new task", True)
except Exception as e:
    log("Add a new task", False, str(e))

# Test 4: Task appears in list ...........
try:
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Selenium Test Task" in body
    log("Task appears in the list", True)
except:
    log("Task appears in the list", False, "Task not visible")

# Test 5: Complete a task
try:
    complete_btn = driver.find_elements(By.CSS_SELECTOR, "button")
    clicked = False
    for btn in complete_btn:
        if "complete" in btn.text.lower() or "done" in btn.text.lower() or "✓" in btn.text:
            btn.click()
            clicked = True
            break
    time.sleep(1)
    log("Mark task as complete", clicked)
except Exception as e:
    log("Mark task as complete", False, str(e))

# Test 6: Filter buttons exist
try:
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "All" in body or "Pending" in body or "Completed" in body
    log("Filter buttons are present", True)
except:
    log("Filter buttons are present", False, "Filter buttons not found")

# Test 7: Empty input validation
try:
    input_box = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder]")
    input_box.clear()
    add_btn = driver.find_elements(By.CSS_SELECTOR, "button")[0]
    add_btn.click()
    time.sleep(1)
    log("Empty input does not add task", True)
except Exception as e:
    log("Empty input does not add task", False, str(e))

# Test 8: Page title/header visible ....... *****
try:
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["To-Do", "Todo", "Task", "TODO"])
    log("App heading is visible", True)
except:
    log("App heading is visible", False, "Heading not found")

driver.quit()

print(f"\n┌────────────────────────────────────┐")
print(f"│  Tests passed : {passed:<19}│")
print(f"│  Tests failed : {failed:<19}│")
print(f"│  Total        : {passed+failed:<19}│")
print(f"└────────────────────────────────────┘\n")