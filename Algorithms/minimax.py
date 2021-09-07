def minimax(position, depth, maximizingPlayer):
    if depth == 0 or gameOver in position:
	    return staticEvaluation of position
    if maximizingPlayer:
        maxEval = -infinity
        for each child in position:
            eval = minimax(child, depth - 1, false)
            maxEval = max(maxEval, eval)
        return maxEval

    else:
        minEval = infinity
        for each child in position:
            eval = minimax(child, depth - 1, true)
            minEval = min(minEval, eval)
        return minEval
