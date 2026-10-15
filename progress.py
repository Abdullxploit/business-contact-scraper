def show_progress(completed, total):
    percentage = int((completed / total) * 100)

    print(
        f"\rProgress: {percentage}% ({completed}/{total})",
        end="",
        flush=True
    )