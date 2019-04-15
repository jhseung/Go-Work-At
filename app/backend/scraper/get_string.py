def main():
    l = []
    com = input("Company Name?")
    url = input("url?")

    print("Result: \n")
    print("python main.py --headless --url \"" + url + "\" --limit 500 -f " + com + "_reviews.csv")

    # python
    # main.py - -headless - -url
    # "https://www.glassdoor.com/Overview/Working-at-Airbnb-EI_IE391850.11,17.htm" - -limit
    # 100 - f
    # airbnb_reviews.csv


if __name__ == '__main__':
    main()