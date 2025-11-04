import io


class SrtProcesser:
    def __init__(self):
        pass

    def generate_srt_obj(self, text_info_list):
        # text_info_list: (text, start_time, end_time)
        # eg: ("hello", 64.5, 73.7)
        # generate srt io.BytesIO
        srt = io.StringIO()
        for idx, (text, start_time, end_time) in enumerate(text_info_list):
            srt.write(f"{idx + 1}\n")
            srt.write(
                f"{self.format_time(start_time)} --> {self.format_time(end_time)}\n"
            )
            srt.write(f"{text}\n\n")

        return srt

    def generate_srt_file(self, text_info_list, srt_path):
        # text_info_list: (text, start_time, end_time)
        # eg: ("hello", 64.5, 73.7)

        with open(srt_path, "w", encoding="utf-8") as f:
            for idx, (text, start_time, end_time) in enumerate(text_info_list):
                f.write(f"{idx + 1}\n")
                f.write(
                    f"{self.format_time(start_time)} --> {self.format_time(end_time)}\n"
                )
                f.write(f"{text}\n\n")

    def format_time(self, seconds):
        millis = int((seconds - int(seconds)) * 1000)
        seconds = int(seconds)
        s = seconds % 60
        m = (seconds // 60) % 60
        h = seconds // 3600
        return f"{h:02}:{m:02}:{s:02},{millis:03}"
