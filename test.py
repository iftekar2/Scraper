from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import json
import time

# # Function to enter user input into Google Flights and scrape flights data
# def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
#     try: 
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

#         # Select trip type (Round Trip or One Way)
#         trip_type_menu = page.query_selector('.VfPpkd-aPP78e')
#         if trip_type_menu:
#             trip_type_menu.click()
#             time.sleep(1)
#             trip_type_options = page.query_selector_all('li[role="option"]')
#             for option in trip_type_options:
#                 option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#                 if trip_type.lower() in option_text.lower():
#                     option.click()
#                     break
#             time.sleep(1)
#         else:
#             print("Trip type menu not found")

#         # Select seat type (Economy, Business, First class)
#         seat_type_menu = page.query_selector('.JQrP8b')
#         if seat_type_menu:
#             seat_type_menu.click()
#             time.sleep(1)
#             seat_type_options = page.query_selector_all('li[role="option"]')
#             for option in seat_type_options:
#                 option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#                 if seat_type.lower() in option_text.lower():
#                     option.click()
#                     break
#             time.sleep(1)
#         else:
#             print("Seat type menu not found")

#         # Enter "From" location
#         from_place_field = page.query_selector_all('.e5F5td')[0]
#         from_place_field.click()
#         time.sleep(1)
#         from_place_field.type(from_place)
#         time.sleep(1)
#         page.keyboard.press('Enter')

#         # Enter "To" location
#         to_place_field = page.query_selector_all('.e5F5td')[1]
#         to_place_field.click()
#         time.sleep(1)
#         to_place_field.type(to_place)
#         time.sleep(1)
#         page.keyboard.press('Enter')

#         # Enter departure date
#         departure_date_field = page.query_selector('[aria-label="Departure"]')
#         if departure_date_field:
#             departure_date_field.click()
#             time.sleep(1)
#             page.keyboard.type(departure_date)
#             time.sleep(1)
#             page.keyboard.press('Tab')  # Move to the return date field if round trip
#         else:
#             print("Departure date field not found")

#         if trip_type.lower() == 'round trip':
#             # Enter return date
#             time.sleep(1)
#             page.keyboard.type(return_date)
#             time.sleep(1)

#             # Click done button
#             done_button = page.query_selector('button[jsname="McfNlf"][aria-label^="Done"]')
#             if done_button:
#                 done_button.click()
#             else:
#                 print("Done button not found")

#         time.sleep(2)  # Wait for the date picker to close

#         time.sleep(5)  # Wait for results to load

#         # Function to load more results
#         def load_more_results():
#             more_results_button = page.query_selector('button[jsname="bZfYPd"]')
#             if more_results_button:
#                 more_results_button.click()
#                 time.sleep(2)
#                 return True
#             return False

#         # Load all results
#         while load_more_results():
#             pass

#         # Scrape all departing flights once
#         parser_departing = LexborHTMLParser(page.content())
#         all_departing_flights_data = scrape_google_flights(parser_departing)

#         # Get all departing flight elements
#         departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')

#         print(f"Number of departing flight elements found: {len(departing_flights)}")
#         print(f"Number of flights in scraped data: {len(all_departing_flights_data[next(iter(all_departing_flights_data.keys()))])}")

#         all_flight_data = []

#         initial_url = page.url

#         # Determine the key for departing flights in the scraped data
#         departing_key = next(iter(all_departing_flights_data.keys()))

#         # Determine the number of flights to actually scrape
#         num_flights_to_scrape = min(len(departing_flights), len(all_departing_flights_data[departing_key]))

#         print(f"Scraping {num_flights_to_scrape} flights...")
        

#         for index in range(len(departing_flights)):
#             print(f"Scraping flight {index + 1} of {len(departing_flights)}")

#             # Get the departing flight data for this index
#             if index < len(all_departing_flights_data[departing_key]):
#                 departing_flight_data = all_departing_flights_data[departing_key][index]
#             else:
#                 print(f"No data available for departing flight at index {index}. Skipping.")
#                 continue

#             try:
#                 # Check if the element is still attached to the DOM
#                 departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')
                
#                 if index < len(departing_flights):
#                     flight_element = departing_flights[index]
                    
#                     # Ensure the element is visible and stable before clicking
#                     flight_element.wait_for_element_state("visible")
#                     flight_element.wait_for_element_state("stable")
#                     flight_element.click()

#                     time.sleep(5)  # Wait for the page to load

#                     # Scrape return flights after selecting a departing flight
#                     parser_return = LexborHTMLParser(page.content())
#                     return_flight_data = scrape_google_flights(parser_return)

#                     # Combine departing and return flight data
#                     combined_data = {
#                         'departing_flight': departing_flight_data,
#                         'return_flights': return_flight_data,
#                         'departing_flight_index': index
#                     }

#                     all_flight_data.append(combined_data)

#                     # Navigate back to the initial departing flights list
#                     page.goto(initial_url)
#                     time.sleep(5)  # Wait for the page to load

#                 else:
#                     print(f"Warning: Flight element at index {index} no longer exists on the page.")
#                     break

#             except Exception as e:
#                 print(f"An error occurred while processing flight {index + 1}: {str(e)}")
#                 continue


#         # Close browser after processing all flights
#         browser.close()
#         return all_flight_data
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return []  # Return an empty list if there's an error

# # Function to parse and scrape Google Flights data
# def scrape_google_flights(parser, parser_return=None):
#     data = {}

#     categories = parser.root.css('.zBTtmb')
#     category_results = parser.root.css('.Rk10dc')

#     for category, category_result in zip(categories, category_results):
#         category_data = []
#         for result in category_result.css('.yR1fYc'):
#             date_elements = result.css('[jscontroller="cNtv4b"] span')
#             departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
#             arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
#             company = result.css_first('.Ir0Voe .sSHqwe').text()
#             duration = result.css_first('.AdWm1c.gvkrdb').text()
#             stops = result.css_first('.EfT7Ae .ogfYpf').text()
#             emissions = result.css_first('.V1iAHe .AdWm1c').text()
#             emission_comparison = result.css_first('.N6PNV').text()
#             price = result.css_first('.U3gSDe .FpEdX span').text()
#             price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None

#             airline_container = result.css_first('.sSHqwe.tPgKwe.ogfYpf')
#             airline_names = [span.text().strip() for span in airline_container.css('span')
#                              if 'Operated by' not in span.text() and not span.attrs]
#             airline_names_str = ', '.join(airline_names)

#             flight_data = {
#                 'departure_date': departure_date,
#                 'arrival_date': arrival_date,
#                 'company': airline_names_str,
#                 'duration': duration,
#                 'stops': stops,
#                 'emissions': emissions,
#                 'emission_comparison': emission_comparison,
#                 'price': price,
#                 'price_type': price_type
#             }

#             airports = result.css_first('.Ak5kof .sSHqwe')
#             service = result.css_first('.hRBhge')

#             if service:
#                 flight_data['service'] = service.text()
#             else:
#                 flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
#                 flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()

#             stop_info = result.css('.sSHqwe.tPgKwe.ogfYpf')
#             stops_data = []

#             for stop in stop_info:
#                 stop_details = stop.attrs.get('aria-label', '')
#                 layovers = stop_details.split('Layover')

#                 for layover in layovers[1:]:
#                     parts = layover.split(' is a ')
#                     if len(parts) > 1:
#                         duration_and_location = parts[1].split(' layover at ')
#                         if len(duration_and_location) == 2:
#                             stop_duration = duration_and_location[0].strip()
#                             stop_location = duration_and_location[1].split(' in ')[0].strip()
#                             stops_data.append({
#                                 'stop_duration': stop_duration,
#                                 'stop_location': stop_location
#                             })

#             flight_data['stops_data'] = stops_data
#             category_data.append(flight_data)

#         data[category.text().lower().replace(' ', '_')] = category_data

#     if parser_return:
#         return_categories = parser_return.root.css('.zBTtmb')
#         return_category_results = parser_return.root.css('.Rk10dc')

#         for return_category, return_category_result in zip(return_categories, return_category_results):
#             return_category_data = []
#             for return_result in return_category_result.css('.yR1fYc'):
#                 date_elements = return_result.css('[jscontroller="cNtv4b"] span')
#                 departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
#                 arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
#                 company = return_result.css_first('.Ir0Voe .sSHqwe').text()
#                 duration = return_result.css_first('.AdWm1c.gvkrdb').text()
#                 stops = return_result.css_first('.EfT7Ae .ogfYpf').text()
#                 emissions = return_result.css_first('.V1iAHe .AdWm1c').text()
#                 emission_comparison = return_result.css_first('.N6PNV').text()
#                 price = return_result.css_first('.U3gSDe .FpEdX span').text()
#                 price_type = return_result.css_first('.U3gSDe .N872Rd').text() if return_result.css_first('.U3gSDe .N872Rd') else None

#                 airline_container = return_result.css_first('.sSHqwe.tPgKwe.ogfYpf')
#                 airline_names = [span.text().strip() for span in airline_container.css('span')
#                                  if 'Operated by' not in span.text() and not span.attrs]
#                 airline_names_str = ', '.join(airline_names)

#                 flight_data = {
#                     'departure_date': departure_date,
#                     'arrival_date': arrival_date,
#                     'company': airline_names_str,
#                     'duration': duration,
#                     'stops': stops,
#                     'emissions': emissions,
#                     'emission_comparison': emission_comparison,
#                     'price': price,
#                     'price_type': price_type
#                 }

#                 airports = return_result.css_first('.Ak5kof .sSHqwe')
#                 service = return_result.css_first('.hRBhge')

#                 if service:
#                     flight_data['service'] = service.text()
#                 else:
#                     flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
#                     flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()

#                 stop_info = return_result.css('.sSHqwe.tPgKwe.ogfYpf')
#                 stops_data = []

#                 for stop in stop_info:
#                     stop_details = stop.attrs.get('aria-label', '')
#                     layovers = stop_details.split('Layover')

#                     for layover in layovers[1:]:
#                         parts = layover.split(' is a ')
#                         if len(parts) > 1:
#                             duration_and_location = parts[1].split(' layover at ')
#                             if len(duration_and_location) == 2:
#                                 stop_duration = duration_and_location[0].strip()
#                                 stop_location = duration_and_location[1].split(' in ')[0].strip()
#                                 stops_data.append({
#                                     'stop_duration': stop_duration,
#                                     'stop_location': stop_location
#                                 })

#                 flight_data['stops_data'] = stops_data
#                 return_category_data.append(flight_data)

#             data[return_category.text().lower().replace(' ', '_')] = return_category_data

#     return data

# # Main function to execute the script
# def main():
#     from_place = 'JFK'
#     to_place = 'LAX'
#     departure_date = '2024-08-14'
#     return_date = '2024-08-31'
#     trip_type = 'Round Trip'
#     seat_type = 'Economy'

#     with sync_playwright() as playwright:
#         all_flight_data = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
        
#     if not all_flight_data:
#         print("No flight data was found.")
#     else:
#         for index, flight_data in enumerate(all_flight_data):
#             print(f"\nDeparting Flight {index + 1}:")
#             print(json.dumps(flight_data, indent=4))

# if __name__ == "__main__":
#     main()




# # Function to enter user input into Google Flights and scrape flights data
# def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
#     try:
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

#         # (Your previous code for entering trip details)

#         time.sleep(5)  # Wait for results to load

#         # Function to scroll down the page and load more results
#         def scroll_and_load_more():
#             while True:
#                 page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
#                 time.sleep(2)  # Wait for scroll to finish and new content to load
#                 if not page.query_selector('button[jsname="bZfYPd"]'):
#                     break
#                 more_results_button = page.query_selector('button[jsname="bZfYPd"]')
#                 if more_results_button:
#                     more_results_button.click()
#                     time.sleep(2)  # Wait for more results to load

#         # Scroll down and load more flights
#         scroll_and_load_more()

#         # Get all departing flight elements after ensuring everything is loaded
#         departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')
#         print(f"Number of departing flight elements found: {len(departing_flights)}")

#         all_flight_data = []

#         initial_url = page.url

#         for index in range(len(departing_flights)):
#             print(f"Scraping flight {index + 1} of {len(departing_flights)}")

#             try:
#                 # Click on the departing flight
#                 departing_flights[index].click()
#                 time.sleep(5)  # Wait for the page to load

#                 # Scrape return flights after selecting a departing flight
#                 parser_return = LexborHTMLParser(page.content())
#                 return_flight_data = scrape_google_flights(parser_return)

#                 # Combine departing and return flight data
#                 combined_data = {
#                     'departing_flight_index': index,
#                     'return_flights': return_flight_data,
#                 }

#                 all_flight_data.append(combined_data)

#                 # Navigate back to the initial departing flights list
#                 page.goto(initial_url)
#                 time.sleep(5)  # Wait for the page to load

#                 # Re-select all departing flights to avoid stale element reference
#                 departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')

#             except Exception as e:
#                 print(f"An error occurred while processing flight {index + 1}: {str(e)}")
#                 continue

#         # Close browser after processing all flights
#         browser.close()
#         return all_flight_data

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return []  # Return an empty list if there's an error


# Function to enter user input into Google Flights and scrape flights data
def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
    try:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

        # (Your previous code for entering trip details)

        time.sleep(5)  # Wait for results to load

        # Function to scroll down the page and load more results
        def scroll_and_load_more():
            while True:
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                time.sleep(2)  # Wait for scroll to finish and new content to load
                if not page.query_selector('button[jsname="bZfYPd"]'):
                    break
                more_results_button = page.query_selector('button[jsname="bZfYPd"]')
                if more_results_button:
                    more_results_button.click()
                    time.sleep(2)  # Wait for more results to load

        # Scroll down and load more flights
        scroll_and_load_more()

        # Get all departing flight elements after ensuring everything is loaded
        departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')
        print(f"Number of departing flight elements found: {len(departing_flights)}")

        all_flight_data = []

        initial_url = page.url

        for index in range(len(departing_flights)):
            print(f"Scraping flight {index + 1} of {len(departing_flights)}")

            try:
                # Click on the departing flight
                departing_flights[index].click()
                time.sleep(5)  # Wait for the page to load

                # Scrape return flights after selecting a departing flight
                parser_return = LexborHTMLParser(page.content())
                return_flight_data = scrape_google_flights(parser_return)

                # Combine departing and return flight data
                combined_data = {
                    'departing_flight_index': index,
                    'return_flights': return_flight_data,
                }

                all_flight_data.append(combined_data)

                # Navigate back to the initial departing flights list
                page.goto(initial_url)
                time.sleep(5)  # Wait for the page to load

                # Re-select all departing flights to avoid stale element reference
                departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')

            except Exception as e:
                print(f"An error occurred while processing flight {index + 1}: {str(e)}")
                continue

        # Close browser after processing all flights
        browser.close()

        # Save the scraped data to a JSON file
        with open('scraped_flight_data.json', 'w') as f:
            json.dump(all_flight_data, f, indent=4)
        
        return all_flight_data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []  # Return an empty list if there's an error



# Function to parse and scrape Google Flights data
def scrape_google_flights(parser, parser_return=None):
    data = {}

    categories = parser.root.css('.zBTtmb')
    category_results = parser.root.css('.Rk10dc')

    for category, category_result in zip(categories, category_results):
        category_data = []
        for result in category_result.css('.yR1fYc'):
            date_elements = result.css('[jscontroller="cNtv4b"] span')
            departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
            arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
            company = result.css_first('.Ir0Voe .sSHqwe').text()
            duration = result.css_first('.AdWm1c.gvkrdb').text()
            stops = result.css_first('.EfT7Ae .ogfYpf').text()
            emissions = result.css_first('.V1iAHe .AdWm1c').text()
            emission_comparison = result.css_first('.N6PNV').text()
            price = result.css_first('.U3gSDe .FpEdX span').text()
            price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None

            airline_container = result.css_first('.sSHqwe.tPgKwe.ogfYpf')
            airline_names = [span.text().strip() for span in airline_container.css('span')
                             if 'Operated by' not in span.text() and not span.attrs]
            airline_names_str = ', '.join(airline_names)

            flight_data = {
                'departure_date': departure_date,
                'arrival_date': arrival_date,
                'company': airline_names_str,
                'duration': duration,
                'stops': stops,
                'emissions': emissions,
                'emission_comparison': emission_comparison,
                'price': price,
                'price_type': price_type
            }

            airports = result.css_first('.Ak5kof .sSHqwe')
            service = result.css_first('.hRBhge')

            if service:
                flight_data['service'] = service.text()
            else:
                flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
                flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()

            stop_info = result.css('.sSHqwe.tPgKwe.ogfYpf')
            stops_data = []

            for stop in stop_info:
                stop_details = stop.attrs.get('aria-label', '')
                layovers = stop_details.split('Layover')

                for layover in layovers[1:]:
                    parts = layover.split(' is a ')
                    if len(parts) > 1:
                        duration_and_location = parts[1].split(' layover at ')
                        if len(duration_and_location) == 2:
                            stop_duration = duration_and_location[0].strip()
                            stop_location = duration_and_location[1].split(' in ')[0].strip()
                            stops_data.append({
                                'stop_duration': stop_duration,
                                'stop_location': stop_location
                            })

            flight_data['stops_data'] = stops_data
            category_data.append(flight_data)

        data[category.text().lower().replace(' ', '_')] = category_data

    if parser_return:
        return_categories = parser_return.root.css('.zBTtmb')
        return_category_results = parser_return.root.css('.Rk10dc')

        for return_category, return_category_result in zip(return_categories, return_category_results):
            return_category_data = []
            for return_result in return_category_result.css('.yR1fYc'):
                date_elements = return_result.css('[jscontroller="cNtv4b"] span')
                departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
                arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
                company = return_result.css_first('.Ir0Voe .sSHqwe').text()
                duration = return_result.css_first('.AdWm1c.gvkrdb').text()
                stops = return_result.css_first('.EfT7Ae .ogfYpf').text()
                emissions = return_result.css_first('.V1iAHe .AdWm1c').text()
                emission_comparison = return_result.css_first('.N6PNV').text()
                price = return_result.css_first('.U3gSDe .FpEdX span').text()
                price_type = return_result.css_first('.U3gSDe .N872Rd').text() if return_result.css_first('.U3gSDe .N872Rd') else None

                airline_container = return_result.css_first('.sSHqwe.tPgKwe.ogfYpf')
                airline_names = [span.text().strip() for span in airline_container.css('span')
                                 if 'Operated by' not in span.text() and not span.attrs]
                airline_names_str = ', '.join(airline_names)

                flight_data = {
                    'departure_date': departure_date,
                    'arrival_date': arrival_date,
                    'company': airline_names_str,
                    'duration': duration,
                    'stops': stops,
                    'emissions': emissions,
                    'emission_comparison': emission_comparison,
                    'price': price,
                    'price_type': price_type
                }

                airports = return_result.css_first('.Ak5kof .sSHqwe')
                service = return_result.css_first('.hRBhge')

                if service:
                    flight_data['service'] = service.text()
                else:
                    flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
                    flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()

                stop_info = return_result.css('.sSHqwe.tPgKwe.ogfYpf')
                stops_data = []

                for stop in stop_info:
                    stop_details = stop.attrs.get('aria-label', '')
                    layovers = stop_details.split('Layover')

                    for layover in layovers[1:]:
                        parts = layover.split(' is a ')
                        if len(parts) > 1:
                            duration_and_location = parts[1].split(' layover at ')
                            if len(duration_and_location) == 2:
                                stop_duration = duration_and_location[0].strip()
                                stop_location = duration_and_location[1].split(' in ')[0].strip()
                                stops_data.append({
                                    'stop_duration': stop_duration,
                                    'stop_location': stop_location
                                })

                flight_data['stops_data'] = stops_data
                return_category_data.append(flight_data)

            data[return_category.text().lower().replace(' ', '_')] = return_category_data

    return data


# Main function to execute the script
def main():
    from_place = 'JFK'
    to_place = 'LAX'
    departure_date = '2024-08-14'
    return_date = '2024-08-31'
    trip_type = 'Round Trip'
    seat_type = 'Economy'

    with sync_playwright() as playwright:
        all_flight_data = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)

    if not all_flight_data:
        print("No flight data was found.")
    else:
        for index, flight_data in enumerate(all_flight_data):
            print(f"\nDeparting Flight {index + 1}:")
            print(json.dumps(flight_data, indent=4))

if __name__ == "__main__":
    main()