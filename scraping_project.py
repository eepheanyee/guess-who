import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
#quotes scraping
BASE_URL = "http://quotes.toscrape.com"
def scrape_quotes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    page_url = True
    while page_url:
        try:
            quote_block = soup.select(".text")
            quote = [q.get_text() for q in quote_block]
            name_block = soup.select(".author") 
            text = [n.get_text() for n in name_block]  
            href_block = soup.find_all("a")
            url = [h.attrs["href"] for h in href_block if h.get_text() == "(about)"]   
            page_url = soup.select(".next")[0].find("a")["href"]
            response = requests.get(f"{BASE_URL}{page_url}")
            soup = BeautifulSoup(response.text, "html.parser")
            all_quotes = [q for q in zip(quote,text,url)]
            # sleep (2)
            return all_quotes
        except IndexError:
            break
#game logic
def start_game(quotes):
    random_quote = choice(quotes)
    hint_response = requests.get(f"{BASE_URL}{random_quote[2]}")
    hint_soup = BeautifulSoup(hint_response.text, "html.parser")
    name = hint_soup.select(".author-title")[0].get_text()
    names = name.split(" ")
    f_name = names[0]
    l_name = names[-1]
    date = hint_soup.select(".author-born-date")[0].get_text()
    location = hint_soup.select(".author-born-location")[0].get_text()
    hint1 = "The author was born on " + date + " " + location
    hint2 = f"The author's first name starts with the letter {f_name[0]}"
    hint3 = f"The author's last name starts with the letter {l_name[0]}"
    hints = [hint1,hint2,hint3]
    guess = 4
    print("Here's a Quote: \n\n")
    print(f"{random_quote[0]} \n\n")
    answer = input(f"Who said this? Guesses remaining: {guess}. ").lower()

    index = 0
    while answer != random_quote[1].lower():    
        guess -= 1
        if guess == 0:
            print(f"Sorry, you lost!  The answer is {random_quote[1]}")
            break
        print(f"Here's a hint: {hints[index]}")
        answer = input(f"Who said this? Guesses remaining: {guess}. ").lower()
        index += 1
    
    if answer == random_quote[1].lower():
        print("That was correct!!  Congratulations!")
    play = ""
    while play not in ("yes", "y", "no", "n"):
        play = input("Do you want to play again?  (y/n): ").lower()
    if play in ("yes", "y"):
        return start_game(quotes)
    else:
        print("Ok GOODBYE")
quotes = scrape_quotes()
start_game(quotes)