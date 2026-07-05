import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = a[i]

    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            dp[i][j] = max(a[i] - dp[i + 1][j], a[j] - dp[i][j - 1])

    diff = dp[0][n - 1] if n > 0 else 0

    if diff > 0:
        print("Player 1 wins")
    elif diff < 0:
        print("Player 2 wins")
    else:
        print("Tie")


if __name__ == "__main__":
    main()
