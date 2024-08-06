from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import json
import time

# This function is going to enter the information the user passes as input into Google Flights
def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
    # This is creating a new browser instance
    browser = playwright.chromium.launch(headless=False)
    # This is opening a chrome page
    page = browser.new_page()
    # This is the page that is being scraped
    page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

    # Select trip type (Round Trip or One Way)
    trip_type_menu = page.query_selector('.VfPpkd-aPP78e')
    if trip_type_menu:
        trip_type_menu.click()
        time.sleep(1)
        trip_type_options = page.query_selector_all('li[role="option"]')
        for option in trip_type_options:
            option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
            if trip_type.lower() in option_text.lower():
                option.click()
                break
        time.sleep(1)
    else:
        print("Trip type menu not found")

    # Select seat type (Economy, Business, First class)
    seat_type_menu = page.query_selector('.JQrP8b')
    if seat_type_menu:
        seat_type_menu.click()
        time.sleep(1)
        seat_type_options = page.query_selector_all('li[role="option"]')
        for option in seat_type_options:
            option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
            print(f"Seat type option found: {option_text}")
            if seat_type.lower() in option_text.lower():
                option.click()
                print(f"seat_type = '{seat_type}'")
                break
        time.sleep(1)
    else:
        print("Seat type menu not found")

    # This is filling up From field
    from_place_field = page.query_selector_all('.e5F5td')[0] # .e5F5td is the From div
    from_place_field.click()
    time.sleep(1)
    from_place_field.type(from_place) # This is entering where we are traveling from
    time.sleep(1)
    page.keyboard.press('Enter')

    # This is filling up To field
    to_place_field = page.query_selector_all('.e5F5td')[1] # .e5F5td is the To div
    to_place_field.click()
    time.sleep(1)
    to_place_field.type(to_place) # This is entering where we are going to
    time.sleep(1)
    page.keyboard.press('Enter')

    # This is filling up Departure Date
    departure_date_field = page.query_selector('[aria-label="Departure"]') # [aria-label="Departure"] this is the departure date field
    if departure_date_field:
        departure_date_field.click()
        time.sleep(1)
        page.keyboard.type(departure_date) # This is entering Departure Date
        time.sleep(1)
        page.keyboard.press('Tab')  # Move to the return date field if round trip
    else:
        print("Departure date field not found")

    if trip_type.lower() == 'round trip':
        # This is filling up Return Date
        time.sleep(1)
        page.keyboard.type(return_date) # This is entering Return Date
        time.sleep(1)

        # Once Departure and Return dates are filled, the done button will be pressed
        done_button = page.query_selector('button[jsname="McfNlf"][aria-label^="Done"]') # This is finding the done button
        if done_button:
            done_button.click()
        else:
            print("Done button not found")

    time.sleep(2)  # Wait for the date picker to close

    time.sleep(5)  # Wait for results to load

    # This is going to scroll to the bottom of the page so more results can be loaded
    for _ in range(3):
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)

        # This is going to parse the page using Selectolax for the data that we are looking for
        parser = LexborHTMLParser(page.content())

        if trip_type.lower() == 'round trip':
            # Locate the element representing the first flight (departure) and click on it to reveal return flights
            first_flight_selector = '.yR1fYc[jsaction*="click:O1htCb"]'
            first_flight = page.query_selector(first_flight_selector)

            if first_flight:
                first_flight.click()
                # Wait for the return flight options to load
                time.sleep(5)

                # Capture the dynamically generated URL for the return flight page
                return_flight_url = page.url  # Capture the dynamically generated URL

                print(f"Return flight URL: {return_flight_url}")  # Optional: For debugging

                # Parse the return flight data
                parser_return = LexborHTMLParser(page.content())

                # After the data is parsed, the browser will be closed
                browser.close()

                # This is returning both the parsed data from the website
                return parser, parser_return
            else:
                print("No departure flight found.")
                browser.close()
                return parser, None
        else:
            # After the data is parsed, the browser will be closed
            browser.close()

            # This is returning the parsed data from the website
            return parser, None
# This function is going to parse and scrape data from Google Flights and store it in a dictionary
def scrape_google_flights(parser, parser_return=None):
    # This dictionary is going to hold the scraped data
    data = {}

    # This is getting all flight categories
    categories = parser.root.css('.zBTtmb')
    # This is getting all flight results
    category_results = parser.root.css('.Rk10dc')

    for category, category_result in zip(categories, category_results):
        # This is going to hold data for each category
        category_data = []

        # This is iterating through each flight result
        for result in category_result.css('.yR1fYc'):
            date_elements = result.css('[jscontroller="cNtv4b"] span')
            departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
            arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
            company = result.css_first('.Ir0Voe .sSHqwe').text() # This is getting airline name
            duration = result.css_first('.AdWm1c.gvkrdb').text() # This is getting flight duration
            stops = result.css_first('.EfT7Ae .ogfYpf').text() # This is getting the number of stops
            emissions = result.css_first('.V1iAHe .AdWm1c').text() # This is getting emissions data
            emission_comparison = result.css_first('.N6PNV').text() # This is getting emission comparison data
            price = result.css_first('.U3gSDe .FpEdX span').text() # This is getting the price
            price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None # This is getting different price types if it is available

            # This is going to hold flight data
            flight_data = {
                'departure_date': departure_date,
                'arrival_date': arrival_date,
                'company': company,
                'duration': duration,
                'stops': stops,
                'emissions': emissions,
                'emission_comparison': emission_comparison,
                'price': price,
                'price_type': price_type
            }

            # This is getting airport information
            airports = result.css_first('.Ak5kof .sSHqwe')
            service = result.css_first('.hRBhge')

            # If service data is available, it will be added to flight data
            if service:
                flight_data['service'] = service.text()
            else:
                flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text() # This is getting departure airport from the user
                flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text() # This is getting arrival airport from the user

            # Adding the code to scrape stop duration and location
            stop_info = result.css('.sSHqwe.tPgKwe.ogfYpf')
            stops_data = []

            for stop in stop_info:
                # Extracting stop duration and location from aria-label
                stop_details = stop.attrs.get('aria-label', '')
                layovers = stop_details.split('Layover')

                for layover in layovers[1:]:  # Skip the first split part as it's empty
                    parts = layover.split(' is a ')
                    if len(parts) > 1:
                        # Further split to get duration and location separately
                        duration_and_location = parts[1].split(' layover at ')
                        if len(duration_and_location) == 2:
                            stop_duration = duration_and_location[0].strip()
                            location_info = duration_and_location[1].strip()
                            # Extract full stop location
                            stop_location = location_info.split(' in ')[0] if ' in ' in location_info else location_info

                            stop_data = {
                                'stop_duration': stop_duration,
                                'stop_location': stop_location
                            }
                            stops_data.append(stop_data)
                    
            flight_data['stops_data'] = stops_data

            # This is adding flight data to category
            category_data.append(flight_data)

        # This is adding the category data to the main dictionary
        data[category.text().lower().replace(' ', '_')] = category_data

    
    if parser_return:
        # This is getting all return flight categories
        return_categories = parser_return.root.css('.zBTtmb')
        # This is getting all return flight results
        return_category_results = parser_return.root.css('.Rk10dc')

        for return_category, return_category_result in zip(return_categories, return_category_results):
            # This is going to hold data for each return category
            return_category_data = []

            # This is iterating through each return flight result
            for return_result in return_category_result.css('.yR1fYc'):
                date_elements = return_result.css('[jscontroller="cNtv4b"] span') # This is finding date information
                departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
                arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
                company = return_result.css_first('.Ir0Voe .sSHqwe').text() # This is getting airline name
                duration = return_result.css_first('.AdWm1c.gvkrdb').text() # This is getting flight duration
                stops = return_result.css_first('.EfT7Ae .ogfYpf').text() # This is getting the number of stops
                emissions = return_result.css_first('.V1iAHe .AdWm1c').text() # This is getting emissions data
                emission_comparison = return_result.css_first('.N6PNV').text() # This is getting emission comparison data
                price = return_result.css_first('.U3gSDe .FpEdX span').text() # This is getting the price
                price_type = return_result.css_first('.U3gSDe .N872Rd').text() if return_result.css_first('.U3gSDe .N872Rd') else None # This is getting different price types if it is available

                # This is going to hold flight data
                return_flight_data = {
                    'departure_date': departure_date,
                    'arrival_date': arrival_date,
                    'company': company,
                    'duration': duration,
                    'stops': stops,
                    'emissions': emissions,
                    'emission_comparison': emission_comparison,
                    'price': price,
                    'price_type': price_type
                }

                # This is getting airport information
                airports = return_result.css_first('.Ak5kof .sSHqwe')
                service = return_result.css_first('.hRBhge')


                # If service data is available, it will be added to flight data
                if service:
                    return_flight_data['service'] = service.text()
                else:
                    return_flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text() # This is getting departure airport from the user
                    return_flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text() # This is getting arrival airport from the user

                # This is adding return flight data to return category
                return_category_data.append(return_flight_data)

                # Adding the code to scrape stop duration and location for return flights
                stop_info = return_result.css('.sSHqwe.tPgKwe.ogfYpf')
                stops_data = []

                for stop in stop_info:
                    # Extracting stop duration and location from aria-label
                    stop_details = stop.attrs.get('aria-label', '')
                    layovers = stop_details.split('Layover')

                    for layover in layovers[1:]:  # Skip the first split part as it's empty
                        parts = layover.split(' is a ')
                        if len(parts) > 1:
                            # Further split to get duration and location separately
                            duration_and_location = parts[1].split(' layover at ')
                            if len(duration_and_location) == 2:
                                stop_duration = duration_and_location[0].strip()
                                location_info = duration_and_location[1].strip()
                                # Extract full stop location
                                stop_location = location_info.split(' in ')[0] if ' in ' in location_info else location_info

                                stop_data = {
                                    'stop_duration': stop_duration,
                                    'stop_location': stop_location
                                }
                                stops_data.append(stop_data)

                return_flight_data['stops_data'] = stops_data

            # This is adding the return category data to the main dictionary
            data[f'return_{return_category.text().lower().replace(" ", "_")}'] = return_category_data

    return data

def main():
    # This is going to take user input
    from_place = input("Enter the departure location: ")
    to_place = input("Enter the destination: ")
    departure_date = input("Enter the departure date (YYYY-MM-DD): ")
    trip_type = input("Enter the trip type (Round Trip or One Way): ")
    seat_type = input("Enter the seat type (Economy, Business, First class): ")
    return_date = ''
    if trip_type.lower() == 'round trip':
        return_date = input("Enter the return date (YYYY-MM-DD): ")

    with sync_playwright() as playwright:
        parser, parser_return = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
        flight_data = scrape_google_flights(parser, parser_return)
        print(json.dumps(flight_data, indent=4))

if __name__ == '__main__':
    main()
