def Summary(count_win:int, count_loss:int, win_percentage:float, win_loss_ratio:float) -> str:
    """
    Analyzes trading strategy profitability based on win percentage and win/loss ratio.
    
    Args:
        win_percentage (float): Percentage of winning trades (0-100)
        win_loss_ratio (float): Ratio of average win to average loss
    
    Returns:
        str: Analysis summary
    """

    # Convert percentage to decimal for calculations
    win_rate = win_percentage / 100
    loss_rate = 1 - win_rate
    
    # Calculate expected value per trade
    # EV = (Win Rate × Win Amount) - (Loss Rate × Loss Amount)
    expected_value = (win_rate * win_loss_ratio) - (loss_rate * 1)
    
    # Profitability thresholds
    break_even_ratio = loss_rate / win_rate  # Minimum ratio needed to break even
    
    summary = ""
    profitability_status = ""
    
    # Main profitability assessment
    if expected_value > 0:
        profitability_status = "PROFITABLE"
        
        if expected_value > 0.3:
            summary = "🟢 HIGHLY PROFITABLE STRATEGY\n\n"
            summary += f"Your strategy shows excellent profitability with a {win_percentage}% win rate and {win_loss_ratio}:1 win/loss ratio. "
            summary += f"The expected value of +{expected_value * 100:.2f}% per trade indicates strong performance. "
            summary += "This combination suggests a well-balanced approach with consistent positive returns."
            
        elif expected_value > 0.1:
            summary = "🟡 MODERATELY PROFITABLE STRATEGY\n\n"
            summary += f"Your strategy is profitable with a {win_percentage}% win rate and {win_loss_ratio}:1 win/loss ratio. "
            summary += f"The expected value of +{expected_value * 100:.2f}% per trade shows positive returns, though there's room for optimization. "
            
        else:
            summary = "🟡 MARGINALLY PROFITABLE STRATEGY\n\n"
            summary += f"Your strategy is barely profitable with a {win_percentage}% win rate and {win_loss_ratio}:1 win/loss ratio. "
            summary += f"The low expected value of +{expected_value * 100:.2f}% per trade suggests minimal edge. "
            summary += "Small changes in market conditions or execution could easily turn this unprofitable."
            
    elif expected_value == 0:
        profitability_status = "BREAK-EVEN"
        summary = "⚪ BREAK-EVEN STRATEGY\n\n"
        summary += f"Your strategy breaks even with a {win_percentage}% win rate and {win_loss_ratio}:1 win/loss ratio. "
        summary += "While you're not losing money, you're also not generating profits after accounting for wins and losses. "
        summary += "Consider strategy refinements to tip the balance toward profitability."
        
    else:
        profitability_status = "UNPROFITABLE"
        
        if expected_value < -0.2:
            summary = "🔴 HIGHLY UNPROFITABLE STRATEGY\n\n"
            summary += f"Your strategy is losing money significantly with a {win_percentage}% win rate and {win_loss_ratio}:1 win/loss ratio. "
            summary += f"The expected value of {expected_value * 100:.2f}% per trade indicates substantial losses over time. "
            summary += "This strategy requires major revision or should be abandoned."
            
        else:
            summary = "🔴 UNPROFITABLE STRATEGY\n\n"
            summary += f"Your strategy is losing money with a {win_percentage}% win rate and {win_loss_ratio}:1 win/loss ratio. "
            summary += f"The expected value of {expected_value * 100:.2f}% per trade shows negative returns. "
            summary += "You need to either increase your win rate or improve your win/loss ratio to achieve profitability."
    
    # Additional insights
    summary += f"\n\n📊 KEY METRICS:\n"
    summary += f"• Total Winners: {count_win}\n"
    summary += f"• Total Losers: {count_loss}\n"
    summary += f"• Win Rate: {win_percentage}%\n"
    summary += f"• Win/Loss Ratio: {win_loss_ratio}:1\n"
    summary += f"• Expected Value: {'+' if expected_value > 0 else ''}{expected_value * 100:.2f}% per trade\n"
    summary += f"• Break-even Ratio Needed: {break_even_ratio:.2f}:1\n"
    
    # Insight
    summary += f"\n💡 KEY INSIGHTS:\n"
    
    if win_loss_ratio < break_even_ratio:
        summary += f"• Your current win/loss ratio ({win_loss_ratio}:1) is below the break-even requirement ({break_even_ratio:.2f}:1)\n"
        summary += "• Focus on improving risk management to increase average wins or reduce average losses\n"
    
    
    if win_percentage > 70 and win_loss_ratio < 1:
        summary += "• You have a high win rate but small wins relative to losses\n"
    
    if win_percentage < 40 and win_loss_ratio > 2:
        summary += "• You have good risk/reward but low win rate\n"
    
    summary += f"• Status: {profitability_status}\n"
    
    return summary.replace('\n', '<br>')
    

if __name__ == '__main__':
    gpt_summary()