#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// Функция для нахождения минимального количества разбиений
int minPal(const string& s) {
    int n = s.length();
    vector<vector<bool>> isPalindrome(n, vector<bool>(n, false));
    vector<int> dp(n);

    // Заполнение массива isPalindrome
    for (int i = 0; i < n; ++i) {
        isPalindrome[i][i] = true; // Каждый символ сам по себе - палиндром
    }

    for (int length = 2; length <= n; ++length) { // Длина подстроки
        for (int i = 0; i <= n - length; ++i) {
            int j = i + length - 1;
            if (s[i] == s[j]) {
                if (length == 2) {
                    isPalindrome[i][j] = true; // Два одинаковых символа
                } else {
                    isPalindrome[i][j] = isPalindrome[i + 1][j - 1]; // Проверяем внутреннюю подстроку
                }
            }
        }
    }

    // Заполнение массива dp
    for (int i = 0; i < n; ++i) {
        if (isPalindrome[0][i]) {
            dp[i] = 0; // Если вся строка до i - палиндром
        } else {
            dp[i] = INT_MAX;
            for (int j = 0; j < i; ++j) {
                if (isPalindrome[j + 1][i]) { // Проверяем подстроку от j+1 до i
                    dp[i] = min(dp[i], dp[j] + 1);
                }
            }
        }
    }

    return dp[n - 1]; // Возвращаем минимальное количество разбиений
}

int main() {
    //string input = "ABCDDDD";
    string input = "IFIFICIFBCB";
    //cout << "Input string: ";
    //cin >> input;

    int result = minPal(input);

    cout << "MIN RAZB NUM: " << result << endl;

    return 0;
}
