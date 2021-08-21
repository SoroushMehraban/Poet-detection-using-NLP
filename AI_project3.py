def colored(r, g, b, text):
    """
    gets text and color as a parameter and returns colored text
    :param r: RED
    :param g: GREEN
    :param b: BLUE
    :param text: given text
    :return: colored text
    """
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def create_two_words_dictionary():
    result = {
        'Ferdowsi': {},
        'Hafez': {},
        'Molavi': {}
    }

    with open('ferdowsi_train.txt', 'r', encoding='utf-8') as ferdowsi_file:
        for line in ferdowsi_file:
            line_words = line.split()
            for i in range(len(line_words) - 1):
                two_words = f"{line_words[i]} {line_words[i + 1]}"
                if two_words in result['Ferdowsi']:
                    result['Ferdowsi'][two_words] += 1
                else:
                    result['Ferdowsi'][two_words] = 1

            # beginning word
            two_words = f"<s> {line_words[0]}"
            if two_words in result['Ferdowsi']:
                result['Ferdowsi'][two_words] += 1
            else:
                result['Ferdowsi'][two_words] = 1

            # ending word
            two_words = f"{line_words[-1]} </s>"
            if two_words in result['Ferdowsi']:
                result['Ferdowsi'][two_words] += 1
            else:
                result['Ferdowsi'][two_words] = 1

    with open('hafez_train.txt', 'r', encoding='utf-8') as hafez_file:
        for line in hafez_file:
            line_words = line.split()
            for i in range(len(line_words) - 1):
                two_words = f"{line_words[i]} {line_words[i + 1]}"
                if two_words in result['Hafez']:
                    result['Hafez'][two_words] += 1
                else:
                    result['Hafez'][two_words] = 1

            # beginning word
            two_words = f"<s> {line_words[0]}"
            if two_words in result['Hafez']:
                result['Hafez'][two_words] += 1
            else:
                result['Hafez'][two_words] = 1

            # ending word
            two_words = f"{line_words[-1]} </s>"
            if two_words in result['Hafez']:
                result['Hafez'][two_words] += 1
            else:
                result['Hafez'][two_words] = 1

    with open('molavi_train.txt', 'r', encoding='utf-8') as molavi_file:
        for line in molavi_file:
            line_words = line.split()
            for i in range(len(line_words) - 1):
                two_words = f"{line_words[i]} {line_words[i + 1]}"
                if two_words in result['Molavi']:
                    result['Molavi'][two_words] += 1
                else:
                    result['Molavi'][two_words] = 1

            # beginning word
            two_words = f"<s> {line_words[0]}"
            if two_words in result['Molavi']:
                result['Molavi'][two_words] += 1
            else:
                result['Molavi'][two_words] = 1

            # ending word
            two_words = f"{line_words[-1]} </s>"
            if two_words in result['Molavi']:
                result['Molavi'][two_words] += 1
            else:
                result['Molavi'][two_words] = 1

    return result


def create_word_dictionary():
    result = {
        'Ferdowsi': {
            '<s>': 0,
            '</s>': 0
        },
        'Hafez': {
            '<s>': 0,
            '</s>': 0
        },
        'Molavi': {
            '<s>': 0,
            '</s>': 0
        }
    }

    with open('ferdowsi_train.txt', 'r', encoding='utf-8') as ferdowsi_file:
        for line in ferdowsi_file:
            for word in line.split():
                if word in result['Ferdowsi']:
                    result['Ferdowsi'][word] += 1
                else:
                    result['Ferdowsi'][word] = 1
            result['Ferdowsi']['<s>'] += 1
            result['Ferdowsi']['</s>'] += 1

    with open('hafez_train.txt', 'r', encoding='utf-8') as hafez_file:
        for line in hafez_file:
            for word in line.split():
                if word in result['Hafez']:
                    result['Hafez'][word] += 1
                else:
                    result['Hafez'][word] = 1
            result['Hafez']['<s>'] += 1
            result['Hafez']['</s>'] += 1

    with open('molavi_train.txt', 'r', encoding='utf-8') as molavi_file:
        for line in molavi_file:
            for word in line.split():
                if word in result['Molavi']:
                    result['Molavi'][word] += 1
                else:
                    result['Molavi'][word] = 1
            result['Molavi']['<s>'] += 1
            result['Molavi']['</s>'] += 1

    return result


def remove_weakest_ones():
    for poet in word_dictionary:
        for word_poet in list(word_dictionary[poet]):
            if word_dictionary[poet][word_poet] < 2:
                del word_dictionary[poet][word_poet]

    for poet in two_words_dictionary:
        for word_poet in list(two_words_dictionary[poet]):
            if two_words_dictionary[poet][word_poet] < 2:
                del two_words_dictionary[poet][word_poet]


def calculate_unigram():
    result = {
        'Ferdowsi': {},
        'Hafez': {},
        'Molavi': {}
    }

    ferdowsi_sum = sum(word_dictionary['Ferdowsi'].values())
    hafez_sum = sum(word_dictionary['Hafez'].values())
    molavi_sum = sum(word_dictionary['Molavi'].values())

    for word in word_dictionary['Ferdowsi']:
        repetition = word_dictionary['Ferdowsi'][word]
        probability = repetition / ferdowsi_sum
        result['Ferdowsi'][word] = probability

    for word in word_dictionary['Hafez']:
        repetition = word_dictionary['Hafez'][word]
        probability = repetition / hafez_sum
        result['Hafez'][word] = probability

    for word in word_dictionary['Molavi']:
        repetition = word_dictionary['Molavi'][word]
        probability = repetition / molavi_sum
        result['Molavi'][word] = probability

    return result


def calculate_bigram():
    result = {
        'Ferdowsi': {
            '</s>': {}
        },
        'Hafez': {
            '</s>': {}
        },
        'Molavi': {
            '</s>': {}
        }
    }
    for poet in two_words_dictionary:
        for two_words in two_words_dictionary[poet]:
            first_word, second_word = two_words.split()
            repetition = two_words_dictionary[poet][two_words]
            condition_repetition = word_dictionary[poet][first_word]
            probability = repetition / condition_repetition
            if second_word in result[poet]:
                result[poet][second_word][first_word] = probability
            else:
                result[poet][second_word] = {first_word: probability}

    return result


def get_test_lines():
    input_test_lines = {}
    with open('test case.txt', 'r', encoding='utf-8') as test_file:
        for index, line in enumerate(test_file):
            number, words = int(line.split()[0]), line.split()[1:]
            if number == 1:
                poet = 'Ferdowsi'
            if number == 2:
                poet = 'Hafez'
            if number == 3:
                poet = 'Molavi'
            input_test_lines[f'line{index + 1}'] = {
                'words': words,
                'poet': poet
            }
    return input_test_lines


def two_words_in_dictionary(words, poet):
    for i in range(len(words) - 1):
        two_words = f'{words[i]} {words[i + 1]}'
        if two_words not in two_words_dictionary[poet]:
            return False

    # beginning
    two_words = f'<s> {words[0]}'
    if two_words not in two_words_dictionary[poet]:
        return False

    # ending
    two_words = f'{words[-1]} </s>'
    if two_words not in two_words_dictionary[poet]:
        return False

    return True


def calculate_probability_of_poet(lambda1, lambda2, lambda3, epsilon, words, poet):
    poet_probability = 1
    if two_words_in_dictionary(words, poet):
        for i in range(len(words) - 1):
            poet_probability *= bigram[poet][words[i + 1]][words[i]]

        poet_probability *= bigram[poet][words[0]]['<s>']  # beginning
        poet_probability *= bigram[poet]['</s>'][words[-1]]  # ending

        return poet_probability

    else:  # one probability is 0 and therefore we should use backoff model
        for i in range(len(words) - 1):
            try:
                p_ci_ci_1 = bigram[poet][words[i + 1]][words[i]]
            except KeyError:  # unknown words
                p_ci_ci_1 = 0
            try:
                p_ci = unigram[poet][words[i + 1]]
            except KeyError:  # unknown words
                p_ci = 0
            poet_probability *= (lambda3 * p_ci_ci_1) + (lambda2 * p_ci) + (lambda1 * epsilon)

        # beginning
        try:
            p_ci_ci_1 = bigram[poet][words[0]]['<s>']
        except KeyError:  # unknown words
            p_ci_ci_1 = 0
        try:
            p_ci = unigram[poet][words[0]]
        except KeyError:  # unknown words
            p_ci = 0
        poet_probability *= (lambda3 * p_ci_ci_1) + (lambda2 * p_ci) + (lambda1 * epsilon)

        # ending
        try:
            p_ci_ci_1 = bigram[poet]['</s>'][words[-1]]
        except KeyError:  # unknown words
            p_ci_ci_1 = 0
        try:
            p_ci = unigram[poet]['</s>']
        except KeyError:  # unknown words
            p_ci = 0
        poet_probability *= (lambda3 * p_ci_ci_1) + (lambda2 * p_ci) + (lambda1 * epsilon)

        return poet_probability


def detect_the_poet(lambda1, lambda2, lambda3, epsilon):
    result = {
        'Ferdowsi': {
            'Correct': 0,
            'Total': 0
        },
        'Hafez': {
            'Correct': 0,
            'Total': 0
        },
        'Molavi': {
            'Correct': 0,
            'Total': 0
        }
    }
    for line in test_lines:
        words = test_lines[line]['words']
        poet = test_lines[line]['poet']
        result[poet]['Total'] += 1

        ferdowsi_probability = calculate_probability_of_poet(lambda1, lambda2, lambda3, epsilon, words, 'Ferdowsi')
        hafez_probability = calculate_probability_of_poet(lambda1, lambda2, lambda3, epsilon, words, 'Hafez')
        molavi_probability = calculate_probability_of_poet(lambda1, lambda2, lambda3, epsilon, words, 'Molavi')

        if ferdowsi_probability > hafez_probability and ferdowsi_probability > molavi_probability:
            if poet == 'Ferdowsi':
                result[poet]['Correct'] += 1
        if hafez_probability > ferdowsi_probability and hafez_probability > molavi_probability:
            if poet == 'Hafez':
                result[poet]['Correct'] += 1
        if molavi_probability > ferdowsi_probability and molavi_probability > hafez_probability:
            if poet == 'Molavi':
                result[poet]['Correct'] += 1

    return result


if __name__ == '__main__':
    """
    Step 1
    """
    print(colored(185, 185, 43, "Creating Dictionary..."))
    word_dictionary = create_word_dictionary()

    two_words_dictionary = create_two_words_dictionary()
    print(colored(67, 196, 67, "Dictionary has created."))
    print("-------------------------")

    print(colored(185, 185, 43, "Removing weakest ones..."))
    remove_weakest_ones()
    print(colored(67, 196, 67, "Weakest ones have removed."))
    print("-------------------------")

    """
    Step 2
    """
    print(colored(185, 185, 43, "Calculating unigram..."))
    unigram = calculate_unigram()
    print(colored(67, 196, 67, "Unigram has calculated."))
    print("-------------------------")

    print(colored(185, 185, 43, "Calculating bigram..."))
    bigram = calculate_bigram()
    print(colored(67, 196, 67, "Bigram has calculated"))
    print("-------------------------")

    """
    Step 3
    """
    test_lines = get_test_lines()

    lambda_1 = 0.2
    lambda_2 = 0.2
    lambda_3 = 0.6
    eps = 1e-06
    print(colored(185, 185, 43,
                  f"Running Algorithm with λ3 = {lambda_3}, λ2 = {lambda_2}, λ1 = {lambda_1}, ε = {eps} ..."))
    result_dictionary = detect_the_poet(lambda_1, lambda_2, lambda_3, eps)
    ferdowsi_precision = result_dictionary['Ferdowsi']['Correct'] / result_dictionary['Ferdowsi']['Total'] * 100
    hafez_precision = result_dictionary['Hafez']['Correct'] / result_dictionary['Hafez']['Total'] * 100
    molavi_precision = result_dictionary['Molavi']['Correct'] / result_dictionary['Molavi']['Total'] * 100
    avg_precision = (ferdowsi_precision + hafez_precision + molavi_precision) / 3
    print(colored(67, 196, 67,
                  f"Ferdowsi: {ferdowsi_precision}%, Hafez: {hafez_precision}%, Molavi: {molavi_precision}%"))
    print(colored(67, 196, 67,
                  f"Average is {avg_precision}%"))
    print("-------------------------")

    lambda_1 = 0.2
    lambda_2 = 0.2
    lambda_3 = 0.6
    eps = 1e-03
    print(colored(185, 185, 43,
                  f"Running Algorithm with λ3 = {lambda_3}, λ2 = {lambda_2}, λ1 = {lambda_1}, ε = {eps} ..."))
    result_dictionary = detect_the_poet(lambda_1, lambda_2, lambda_3, eps)
    ferdowsi_precision = result_dictionary['Ferdowsi']['Correct'] / result_dictionary['Ferdowsi']['Total'] * 100
    hafez_precision = result_dictionary['Hafez']['Correct'] / result_dictionary['Hafez']['Total'] * 100
    molavi_precision = result_dictionary['Molavi']['Correct'] / result_dictionary['Molavi']['Total'] * 100
    avg_precision = (ferdowsi_precision + hafez_precision + molavi_precision) / 3
    print(colored(67, 196, 67,
                  f"Ferdowsi: {ferdowsi_precision}%, Hafez: {hafez_precision}%, Molavi: {molavi_precision}%"))
    print(colored(67, 196, 67,
                  f"Average is {avg_precision}%"))
    print("-------------------------")

    lambda_1 = 0.33
    lambda_2 = 0.33
    lambda_3 = 0.33
    eps = 1e-06
    print(colored(185, 185, 43,
                  f"Running Algorithm with λ3 = {lambda_3}, λ2 = {lambda_2}, λ1 = {lambda_1}, ε = {eps} ..."))
    result_dictionary = detect_the_poet(lambda_1, lambda_2, lambda_3, eps)
    ferdowsi_precision = result_dictionary['Ferdowsi']['Correct'] / result_dictionary['Ferdowsi']['Total'] * 100
    hafez_precision = result_dictionary['Hafez']['Correct'] / result_dictionary['Hafez']['Total'] * 100
    molavi_precision = result_dictionary['Molavi']['Correct'] / result_dictionary['Molavi']['Total'] * 100
    avg_precision = (ferdowsi_precision + hafez_precision + molavi_precision) / 3
    print(colored(67, 196, 67,
                  f"Ferdowsi: {ferdowsi_precision}%, Hafez: {hafez_precision}%, Molavi: {molavi_precision}%"))
    print(colored(67, 196, 67,
                  f"Average is {avg_precision}%"))
    print("-------------------------")

    lambda_1 = 0.33
    lambda_2 = 0.33
    lambda_3 = 0.33
    eps = 1e-03
    print(colored(185, 185, 43,
                  f"Running Algorithm with λ3 = {lambda_3}, λ2 = {lambda_2}, λ1 = {lambda_1}, ε = {eps} ..."))
    result_dictionary = detect_the_poet(lambda_1, lambda_2, lambda_3, eps)
    ferdowsi_precision = result_dictionary['Ferdowsi']['Correct'] / result_dictionary['Ferdowsi']['Total'] * 100
    hafez_precision = result_dictionary['Hafez']['Correct'] / result_dictionary['Hafez']['Total'] * 100
    molavi_precision = result_dictionary['Molavi']['Correct'] / result_dictionary['Molavi']['Total'] * 100
    avg_precision = (ferdowsi_precision + hafez_precision + molavi_precision) / 3
    print(colored(67, 196, 67,
                  f"Ferdowsi: {ferdowsi_precision}%, Hafez: {hafez_precision}%, Molavi: {molavi_precision}%"))
    print(colored(67, 196, 67,
                  f"Average is {avg_precision}%"))
