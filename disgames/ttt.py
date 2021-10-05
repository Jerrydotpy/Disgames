import discord
from discord.ext import commands
from .Board import Board
from .utils import edit_board, format_board

class TTT(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def MakeMove(self, answer, board, turn):
		bord = eval(str(board))
		if answer not in ['11','12','13','21','22','23','31','32','33']:
			return (False, f'Invalid Syntax: {answer} isn\'t a valid place, Please try again')
		else:
			if bord[int(answer[0])][int(answer[1])] != board.seperator:
				return (False, f'Invalid Syntax: {answer} has already been chosen, Please try again')
			else:
				return (True, edit_board(board, [answer], turn))

	def HasWon(self, board, turn):
		BLANK = board.seperator
		bord = eval(str(board))
		h = 0
		for i in bord:
			for thing in i:
				if thing != BLANK:
					h += 1
		if h == 16:
			return (True, "tie")
		for i in range(1,4):

		    if (bord[i][1] == bord[i][2] == bord[i][3]) and bord[i][1] != BLANK:
		        return (True, turn)
		    if (bord[1][i] == bord[2][i] == bord[3][i]) and bord[1][i] != BLANK:
		        return (True, turn)

		if (bord[1][1] == bord[2][2] == bord[3][3]) and bord[1][1] != BLANK:
		    return (True, turn)
		   
		if (bord[1][3] == bord[2][2] == bord[3][1]) and bord[1][3] != BLANK:
		    return (True, turn)
		   
		return (False, 'h')

	@commands.command(aliases=['ttt'])
	async def tictactoe(self, member:discord.Member):
		if member.bot or member == ctx.author:
			return await ctx.send(f"Invalid Syntax: Can't play against {member.display_name}")
		turn = ctx.author
		board = Board(3,3,'|')
		embed = discord.Embed(title='TicTacToe', description=f'turn: `{turn.display_name}`\n```{format_board(board)}\n```')
		msg = await ctx.send(embed=embed)
		while True:
			inp = await self.bot.wait_for('message', check = lambda m: m.author == turn and m.channel == ctx.channel)
			if inp.content == 'cancel':
				return await ctx.send("Cancelled the game")
			outp = self.MakeMove(inp.content, board, 'x' if turn == ctx.author else 'o')
			if outp[0]:
				board = outp[1]
			else:
				await ctx.send(outp[1])
				continue
			h = self.HasWon(board, 'x' if turn == ctx.author else 'o')
			if h[0]:
				return await ctx.send(embed=discord.Embed(title='TicTacToe', description=f'winnder: `{'tie' if h[1] == 'tie' else (ctx.author.display_name if h[1] == 'x' else member.display_name)}`\n```{format_board(board)}\n```'))
			turn = member if turn == ctx.author else ctx.author
			await msg.edit(embed=discord.Embed(title='TicTacToe', description=f'turn: `{turn.display_name}`\n```{format_board(board)}\n```'))

def setup(bot):
	bot.add_cog(TTT(bot))