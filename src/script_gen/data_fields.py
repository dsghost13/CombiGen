class TextEntryHandler:
    DATA = {
        "source_cores": [],
        "source_subs": [],
        "sink_cores": [],
        "sink_subs": [],
        "linkers": [],
        "arrow_pushing": "",
        "pareto_fronts": [],
        "output_proportion": 0.01
    }

    RAW = {
        "source_subs": [],
        "sink_subs": []
    }

    @staticmethod
    def update_field(field, text):
        if field == "arrow_pushing":
            TextEntryHandler.DATA[field] = TextEntryHandler.clean_text(text)
        elif field == "output_proportion":
            try:
                output_proportion = float(text) if float(text) <= 1.0 else 1.0
                TextEntryHandler.DATA[field] = output_proportion
            except:
                pass
        else:
            text_cleaned = TextEntryHandler.clean_text(text)
            TextEntryHandler.DATA[field] = TextEntryHandler.parse_text(text_cleaned)
            if field in TextEntryHandler.RAW.keys():
                TextEntryHandler.RAW[field] = text_cleaned

    @staticmethod
    def clean_text(text_entries):
        if text_entries is None:
            return None

        chars_to_remove = "'\"\n\t"
        translation_table = str.maketrans('', '', chars_to_remove)

        if isinstance(text_entries, list):
            text_cleaned = []
            for text_entry in text_entries:
                text_cleaned.append(text_entry.translate(translation_table))
        else:
            text_cleaned = text_entries.translate(translation_table)
        return text_cleaned

    @staticmethod
    def parse_text(text_entries):
        if text_entries is None:
            return []

        if isinstance(text_entries, list):
            text_parsed = []
            for text_entry in text_entries:
                text_parsed.append([text.strip() for text in text_entry.split(',')])
        else:
            text_parsed = [text.strip() for text in text_entries.split(',')]
        return text_parsed