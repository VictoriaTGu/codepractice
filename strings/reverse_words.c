/* Example of an answer given on quora
 * First reverse the characters, then
 * reverse the words
 * Note: needs a simple swap function
 */
void reverse_word_order_in_place(char* str) {
    int len = strlen(str);
    // reverse string
    for (int i = 0; i < len - i - 1; i++) {
        swap(str[i], str[len - i - 1]);
    }

    // reverse words
    int x = -1;
    for (int i = 0; i < len; i++) {
        if (str[i] == ' ') {
            for (int j = x + 1; j < i - j + x; j++) {
                swap(str[j], str[i - j + x]);
            }
            x = i;
        }
    }
}
