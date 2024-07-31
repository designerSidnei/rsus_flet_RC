def find_col(plan, texto):
    for c in plan[1]:
        if str(c.value).strip().lower() in texto:
            return c.column
