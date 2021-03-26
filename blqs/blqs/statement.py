from blqs import block_stack


class Statement:
    """Statements are the basic building blocks of a blqs program.

    If statement are created within the context of a `Block`, then the
    statement constructure adds this statement to the block.

    ```
    with blqs.Block() as b:
        MyStatement1()
        MyStatement2()
    # b will contain MyStatement1 and MyStatement2
    assert b == [MyStatement1(), MyStatement(2)]
    ```
    """

    def __init__(self):
        # When in a block context, always append the statement on creation.
        if (current_block := block_stack.get_current_block()) is not None:
            current_block.append(self)
