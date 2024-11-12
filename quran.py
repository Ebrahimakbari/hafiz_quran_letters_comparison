import re
from collections import Counter
import matplotlib.pyplot as plt



def normalize_arabic_letters(text):
    text = text.replace("ئ", "ء").replace("إ", "ء").replace("أ", "ء").replace("ؤ", "ء")
    text = text.replace("ء", "")
    text = text.replace("ى", "ي").replace("ـ", "ي")
    text = text.replace("ة", "ه")
    text = text.replace("ٱ", "ا")
    return text


def read_quran_text(file_path, fraction=1.0):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    total_lines = len(lines)
    lines_to_read = int(total_lines * fraction)  
    full_text = ''.join(lines[:lines_to_read])
    return full_text


def calculate_letter_probabilities(file_path, fraction=1.0):
    text = read_quran_text(file_path, fraction=fraction)
    # حذف کاراکترهای غیر از حروف عربی
    arabic_letters_pattern = r'[^ء-ي]'
    clean_text = re.sub(arabic_letters_pattern, '', text)
    # جایگزینی حروف هم‌ارز
    normalized_text = normalize_arabic_letters(clean_text)
    # شمارش تعداد تکرار هر حرف
    letter_frequency = Counter(normalized_text)
    # محاسبه احتمال نسبی هر حرف
    total_count = sum(letter_frequency.values())
    letter_probabilities = {letter: count / total_count for letter,
                            count in letter_frequency.items()}
    return letter_probabilities


def plot_probability_density_comparison(file_path, fractions, output_image_path):
    # ترتیب حروف الفبای عربی
    arabic_alphabet = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
    plt.figure(figsize=(12, 6))
    colors = ['blue', 'green', 'red']  # رنگ‌های متفاوت برای هر مقدار fraction
    markers = ['o', 's', '^']          # نشانه‌های متفاوت برای هر مقدار fraction
    for i, fraction in enumerate(fractions):
        # محاسبه توزیع احتمال برای هر fraction
        letter_probabilities = calculate_letter_probabilities(file_path,
                                                                fraction=fraction)
        # مرتب‌سازی احتمالات بر اساس ترتیب الفبای عربی
        sorted_probabilities = [letter_probabilities.get(letter, 0) for letter in arabic_alphabet]
        # رسم نمودار برای این fraction
        plt.plot(arabic_alphabet, sorted_probabilities, label=f'Fraction = {fraction}', 
                color=colors[i], marker=markers[i], linestyle='-', markersize=5)
        plt.fill_between(arabic_alphabet, sorted_probabilities, color=colors[i], alpha=0.2)

    plt.xlabel("Letters")
    plt.ylabel("Relative probability")
    plt.title("Comparison based on different Fraction (quran)")
    plt.legend()
    plt.xticks(rotation=90)
    plt.savefig(output_image_path, format='png', dpi=300)
    plt.show()


file_path = 'quran.txt'
output_image_path = 'letter_probability_density_quran_comparison.png'
fractions_to_compare = [1.0, 0.5, 0.25]
plot_probability_density_comparison(file_path, fractions_to_compare,
                                    output_image_path)
