def calculate_risk_score(row):
    score = 0

    if row['login_hour'] < 6 or row['login_hour'] > 22:
        score += 20
    if row['files_accessed'] > 100:
        score += 20
    if row['files_downloaded'] > 100:
        score += 25
    if row['failed_logins'] > 3:
        score += 15
    if row['usb_used'] == 1:
        score += 10
    if row['sensitive_access'] == 1:
        score += 20
    if row['network_uploads'] > 100:
        score += 15

    return min(score, 100)

def get_risk_level(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"
