
def extractToken(text, tag_start, tag_end):
    start = text.find(tag_start) + len(tag_start)
    end = text.find(tag_end, start)
    if start < 0 or end < 0:
        return None
    return text[start:end]

def extractJsfState(html):
    state = extractToken(html, '<input type="hidden" name="javax.faces.ViewState"'\
                 ' id="javax.faces.ViewState" value="', '"')
    if not state:
        raise ValueError('No JSF state found in the page.')
    if not state.startswith('j_id') or len(state)>10:
        raise ValueError('Invalid JSF State found: %s.' % str(state))
    return state
