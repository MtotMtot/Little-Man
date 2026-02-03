from re import split
from openai import chat
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from Chatbot import chat
import flet as ft


# Scrape the website
def scrape_target_website(target_url):
    dom_content = scrape_website(target_url)
    body_content = extract_body_content(dom_content)
    cleaned_content = clean_body_content(body_content)
    split_content = split_dom_content(cleaned_content)
    return split_content

def main(page: ft.Page):

    # Default url
    url = "https://mycatlikescheese.co.uk/"
    website_content = []

    # Page elements
    page.title = "Chatbot Demo"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    chat_window = ft.ListView(
            spacing = 10,
            padding = 20,
            width = 400,
            height=700,
            auto_scroll=True,
            controls=[ft.Text()]
            )
   

    # Url submission
    def handle_button_click(e: ft.Event[ft.Button] | ft.Event[ft.TextField]):
        nonlocal website_content
        if (url_field.value != ""):
            try:
                website_content = scrape_target_website(url_field.value)
                url_field.value = "Scraped website!"
            except Exception as e:
                url_field.value = (f"[Error scraping website]: {e}")
        chat_window.controls.append(ft.Text("Assistant: What would you like to ask me?"))
        page.update()
    
        # Chat loop
    def handle_chat_submission(e: ft.Event[ft.TextField]):
        nonlocal website_content
        if user_input.value not in {"exit", "quit"}:
            chat_window.controls.append(ft.Text(f"You: {user_input.value}"))
            response = chat(website_content, user_input.value)
            chat_window.controls.append(ft.Text(f"Assistant: {response}"))
            user_input.value = ""
        page.update()
            
        
    # Page contents
    page.add(
        url_field := ft.TextField(label="Enter Url Here", hint_text="Example https://mycatlikescheese.co.uk/", on_submit=handle_button_click),
        ft.Button(content="Sumbit", on_click=handle_button_click),
        ft.Container(
            content = chat_window,
            bgcolor=ft.Colors.GREY_500,
            ),
        user_input := ft.TextField(label="Ask me anything", hint_text="Enter question here" ,on_submit=handle_chat_submission)
        )

ft.run(main, view=ft.AppView.WEB_BROWSER)