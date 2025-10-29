import os, subprocess, shutil

def process_all(input_folder, output_folder, model, prompt,
                delete_original=False, move_original_to=None,
                func=None, next_y=None, next_n=None):
    
    os.makedirs(output_folder, exist_ok=True)
    if move_original_to:
        os.makedirs(move_original_to, exist_ok=True)

    for fname in os.listdir(input_folder):
        fpath = os.path.join(input_folder, fname)
        if not os.path.isfile(fpath):
            continue

        print(f"[Processor] Working on: {fname}")

        # read input
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # choose mode
        if func:
            output = func(content, fname)
        else:
            cmd = ["ollama", "run", model]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            output, _ = proc.communicate(input=f"{prompt}\n\n{content}")

        # save result
        out_path = os.path.join(output_folder, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)

        # handle original file
        if delete_original:
            os.remove(fpath)
            print(f"[Processor] Deleted original {fname}")
        elif move_original_to:
            shutil.move(fpath, os.path.join(move_original_to, fname))
            print(f"[Processor] Moved original → {move_original_to}")

        print(f"[Processor] Saved result → {out_path}")

       