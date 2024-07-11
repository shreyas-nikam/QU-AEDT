# Import the required libraries
import html
import re
import streamlit as st

def format_message(text):
    """
    This function is used to format the messages in the chatbot UI.

    Args:
    text (str): The text to be formatted.

    Returns:
    str: The formatted text.
    """
    # Split the text into text blocks and code blocks
    text_blocks = re.split(r"```[\s\S]*?```", text)
    text_blocks = [html.escape(block) for block in text_blocks]

    code_blocks = re.findall(r"```([\s\S]*?)```", text)

    # Combine the text and code blocks
    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f'<pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>'

    return formatted_text


def display_on_chat(text, is_user=False):
    """
    This function is used to display the messages in the chatbot UI.

    Args:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or not.

    """

    # If the message is from the user, display the message on the right side
    if is_user:

        # Get the avataar for the user
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=LongHairStraight&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=Red&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light"
        avatar_class = "user-avatar"
        
        # Style the message
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"


        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                </div>
                """,
            unsafe_allow_html=True,
        )

    # If the message is from the bot, display the message on the left side
    else:

        # Get the avataar for the bot
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=Hat&accessoriesType=Prescription02&facialHairType=BeardLight&facialHairColor=Black&clotheType=BlazerSweater&eyeType=Happy&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
        avatar_class = "bot-avatar"

        # Style the message
        message_alignment = "flex-start"
        message_bg_color = "#71797E"

        text = format_message(text)

        st.markdown(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                </div>
                """,
            unsafe_allow_html=True,
        )