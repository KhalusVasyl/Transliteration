def transliterate_ukrainian(name: str) -> str:
    rules = {
        'А': 'A', 'a': 'a',
        'Б': 'B', 'б': 'b',
        'В': 'V', 'в': 'v',
        'Г': 'H', 'г': 'h',
        'Ґ': 'G', 'ґ': 'g',
        'Д': 'D', 'д': 'd',
        'Е': 'E', 'е': 'e',
        'Є': 'Ye', 'є': 'ie',
        'Ж': 'Zh', 'ж': 'zh',
        'З': 'Z', 'з': 'z',
        'И': 'Y', 'и': 'y',
        'І': 'I', 'і': 'i',
        'Ї': 'Yi', 'ї': 'i',
        'Й': 'Y', 'й': 'i',
        'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l',
        'М': 'M', 'м': 'm',
        'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o',
        'П': 'P', 'п': 'p',
        'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's',
        'Т': 'T', 'т': 't',
        'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f',
        'Х': 'Kh', 'х': 'kh',
        'Ц': 'Ts', 'ц': 'ts',
        'Ч': 'Ch', 'ч': 'ch',
        'Ш': 'Sh', 'ш': 'sh',
        'Щ': 'Shch', 'щ': 'shch',
        'Ю': 'Yu', 'ю': 'iu',
        'Я': 'Ya', 'я': 'ia',
        'Ь': '', 'ь': '',
    }

    # We remove all types of apostrophes
    def remove_apostrophes(text: str) -> str:
        apostrophes = ["'", "’", "‘", "ʼ", "`", "´", "ʹ"]
        for a in apostrophes:
            text = text.replace(a, "")
        return text

    clean_name = remove_apostrophes(name)


    result = ""
    for i, ch in enumerate(clean_name):
        if ch in rules:
            val = rules[ch]
            if isinstance(val, tuple):
                # Beginning of a word or after a non-alphabetic character = uppercase version
                if i == 0 or not clean_name[i-1].isalpha():
                    result += val[0]
                else:
                    result += val[1]
            else:
                result += val
        else:
            result += ch
    return result


def transliterate_full_name(full_name: str) -> str:
    parts = full_name.strip().split()
    return ' '.join(transliterate_ukrainian(part) for part in parts)


def transliterate_vcf(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result_lines = []
    for line in lines:
        if line.startswith('FN:'):
            original_name = line[3:].strip()
            transliterated_name = transliterate_full_name(original_name)
            result_lines.append(f"FN:{transliterated_name}\n")
        elif line.startswith('N:'):
            parts = line[2:].strip().split(';')
            parts_translit = [transliterate_full_name(part) if part else '' for part in parts]
            result_lines.append(f"N:{';'.join(parts_translit)}\n")
        else:
            result_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(result_lines)

    print(f"Done! The file with the transliteration has been saved: {output_file}")

if __name__ == "__main__":
    input_vcf = input("Enter the path to the input VCF file: ")
    output_vcf = input("Enter the path to save the output VCF file: ")
    transliterate_vcf(input_vcf, output_vcf)
