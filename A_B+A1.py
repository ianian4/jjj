from simple_watcher import process_all
import subprocess


# Step A → B
process_all(
    input_folder="data/A",
    output_folder="data/B",
    model="llama3.1:8b",
    prompt="answer with excactly 25 words, each separated by one space. pick 25 words that give great context for the following text: ",
    move_original_to="data/A1",
)

# Trigger next step (non-blocking)
subprocess.Popen(["python", "B_C.py"])
subprocess.Popen(["python", "A1_B1.py"])
