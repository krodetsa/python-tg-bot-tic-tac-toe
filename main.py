from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def display_board(self):
        return f"{self.board[0]} | {self.board[1]} | {self.board[2]}\n" \
               f"---------\n" \
               f"{self.board[3]} | {self.board[4]} | {self.board[5]}\n" \
               f"---------\n" \
               f"{self.board[6]} | {self.board[7]} | {self.board[8]}"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Tic-Tac-Toe! Type /play to start a new game.")

def play(update: Update, context: CallbackContext) -> None:
    game = TicTacToeGame()
    context.user_data['game'] = game
    update.message.reply_text(game.display_board())
    update.message.reply_text(f"{game.current_player}'s turn. Type /move <position> to make a move.")

def move(update: Update, context: CallbackContext) -> None:
    game = context.user_data['game']
    position = int(context.args[0]) - 1

    if game.board[position] == ' ':
        game.board[position] = game.current_player
        update.message.reply_text(game.display_board())

        if check_winner(game.board, game.current_player):
            update.message.reply_text(f"Player {game.current_player} wins!")
            del context.user_data['game']
        elif ' ' not in game.board:
            update.message.reply_text("It's a draw!")
            del context.user_data['game']
        else:
            game.current_player = 'O' if game.current_player == 'X' else 'X'
            update.message.reply_text(f"{game.current_player}'s turn. Type /move <position> to make a move.")
    else:
        update.message.reply_text("Invalid move. The position is already occupied. Try again.")

def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    return (any(all(board[i] == player for i in range(j, j + 3)) for j in range(0, 9, 3)) or
            any(all(board[i] == player for i in range(j, 9, 3)) for j in range(3)) or
            all(board[i] == player for i in range(0, 9, 4)) or
            all(board[i] == player for i in range(2, 7, 2)))

def main():
    updater = Updater("BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("move", move, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
