# Original code was taken from
# https://github.com/ankitects/anki/blob/main/qt/aqt/deckbrowser.py

from aqt.deckbrowser import DeckBrowser, RenderDeckNodeContext
from anki.decks import DeckTreeNode
import html


def _render_deck_node_mod(self, node: DeckTreeNode, ctx: RenderDeckNodeContext) -> str:
    if node.collapsed:
        prefix = "+"
    else:
        prefix = "-"

    def indent() -> str:
        return "&nbsp;" * 6 * (node.level - 1)

    if node.deck_id == ctx.current_deck_id:
        klass = "deck current"
    else:
        klass = "deck"

    buf = (
        "<tr class='%s' id='%d' onclick='if(event.shiftKey) return pycmd(\"select:%d\")'>"
        % (
            klass,
            node.deck_id,
            node.deck_id,
        )
    )
    # deck link
    if node.children:
        collapse = (
            "<a class=collapse href=# onclick='return pycmd(\"collapse:%d\")'>%s</a>"
            % (node.deck_id, prefix)
        )
    else:
        collapse = "<span class=collapse></span>"
    if node.filtered:
        extraclass = "filtered"
    else:
        extraclass = ""
    buf += """

    <td class=decktd colspan=5>%s%s<a class="deck %s"
    href=# onclick="return pycmd('open:%d')">%s</a></td>""" % (
        indent(),
        collapse,
        extraclass,
        node.deck_id,
        html.escape(node.name),
    )

    # due counts
    def nonzeroColour(cnt: int, uncapped: int, klass: str) -> str:
        is_parent = not node.collapsed and len(node.children) != 0

        if is_parent or not cnt:
            klass = 'zero-count' 

        text = f'<span class="{klass}">{cnt}</span>'

        remain = max(0, uncapped - cnt)

        if remain:
            text += f' <span class="zero-count">({remain})</span>'

        return text

    dnew = nonzeroColour(node.new_count, node.new_uncapped, "new-count")
    review = nonzeroColour(node.review_count, node.review_uncapped, "review-count")
    learn = nonzeroColour(node.learn_count, 0, "learn-count")

    buf += ("<td align=end>%s</td>" * 3) % (
        dnew,
        learn,
        review,
    )
    # options
    buf += (
        "<td align=center class=opts><a onclick='return pycmd(\"opts:%d\");'>"
        "<img src='/_anki/imgs/gears.svg' class=gears></a></td></tr>" % node.deck_id
    )
    # children
    if not node.collapsed:
        for child in node.children:
            buf += self._render_deck_node(child, ctx)
    return buf

DeckBrowser._render_deck_node = _render_deck_node_mod
