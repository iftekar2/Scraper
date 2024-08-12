# from playwright.sync_api import sync_playwright
# from selectolax.lexbor import LexborHTMLParser
# import json
# import time

# # This function is going to enter the information the user passes as input into Google Flights
# def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
#     # This is creating a new browser instance
#     browser = playwright.chromium.launch(headless=False)
#     # This is opening a chrome page
#     page = browser.new_page()
#     # This is the page that is being scraped
#     page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

#     # Select trip type (Round Trip or One Way)
#     trip_type_menu = page.query_selector('.VfPpkd-aPP78e')
#     if trip_type_menu:
#         trip_type_menu.click()
#         time.sleep(1)
#         trip_type_options = page.query_selector_all('li[role="option"]')
#         for option in trip_type_options:
#             option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#             if trip_type.lower() in option_text.lower():
#                 option.click()
#                 break
#         time.sleep(1)
#     else:
#         print("Trip type menu not found")

#     # Select seat type (Economy, Business, First class)
#     seat_type_menu = page.query_selector('.JQrP8b')
#     if seat_type_menu:
#         seat_type_menu.click()
#         time.sleep(1)
#         seat_type_options = page.query_selector_all('li[role="option"]')
#         for option in seat_type_options:
#             option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#             print(f"Seat type option found: {option_text}")
#             if seat_type.lower() in option_text.lower():
#                 option.click()
#                 print(f"seat_type = '{seat_type}'")
#                 break
#         time.sleep(1)
#     else:
#         print("Seat type menu not found")

#     # This is filling up From field
#     from_place_field = page.query_selector_all('.e5F5td')[0] # .e5F5td is the From div
#     from_place_field.click()
#     time.sleep(1)
#     from_place_field.type(from_place) # This is entering where we are traveling from
#     time.sleep(1)
#     page.keyboard.press('Enter')

#     # This is filling up To field
#     to_place_field = page.query_selector_all('.e5F5td')[1] # .e5F5td is the To div
#     to_place_field.click()
#     time.sleep(1)
#     to_place_field.type(to_place) # This is entering where we are going to
#     time.sleep(1)
#     page.keyboard.press('Enter')

#     # This is filling up Departure Date
#     departure_date_field = page.query_selector('[aria-label="Departure"]') # [aria-label="Departure"] this is the departure date field
#     if departure_date_field:
#         departure_date_field.click()
#         time.sleep(1)
#         page.keyboard.type(departure_date) # This is entering Departure Date
#         time.sleep(1)
#         page.keyboard.press('Tab')  # Move to the return date field if round trip
#     else:
#         print("Departure date field not found")

#     if trip_type.lower() == 'round trip':
#         # This is filling up Return Date
#         time.sleep(1)
#         page.keyboard.type(return_date) # This is entering Return Date
#         time.sleep(1)

#         # Once Departure and Return dates are filled, the done button will be pressed
#         done_button = page.query_selector('button[jsname="McfNlf"][aria-label^="Done"]') # This is finding the done button
#         if done_button:
#             done_button.click()
#         else:
#             print("Done button not found")

#     time.sleep(2)  # Wait for the date picker to close

#     time.sleep(5)  # Wait for results to load

#     # This is going to scroll to the bottom of the page so more results can be loaded
#     for _ in range(3):
#         page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
#         time.sleep(2)

#         # This is going to parse the page using Selectolax for the data that we are looking for
#         parser = LexborHTMLParser(page.content())

#         if trip_type.lower() == 'round trip':
#             # Locate the element representing the first flight (departure) and click on it to reveal return flights
#             first_flight_selector = '.yR1fYc[jsaction*="click:O1htCb"]'
#             first_flight = page.query_selector(first_flight_selector)

#             if first_flight:
#                 first_flight.click()
#                 # Wait for the return flight options to load
#                 time.sleep(5)

#                 # Capture the dynamically generated URL for the return flight page
#                 return_flight_url = page.url  # Capture the dynamically generated URL

#                 # print(f"Return flight URL: {return_flight_url}")  # Optional: For debugging

#                 # Parse the return flight data
#                 parser_return = LexborHTMLParser(page.content())

#                 # After the data is parsed, the browser will be closed
#                 browser.close()

#                 # This is returning both the parsed data from the website
#                 return parser, parser_return
#             else:
#                 print("No departure flight found.")
#                 browser.close()
#                 return parser, None
#         else:
#             # After the data is parsed, the browser will be closed
#             browser.close()

#             # This is returning the parsed data from the website
#             return parser, None
# # This function is going to parse and scrape data from Google Flights and store it in a dictionary
# def scrape_google_flights(parser, parser_return=None):
#     # This dictionary is going to hold the scraped data
#     data = {}

#     # This is getting all flight categories
#     categories = parser.root.css('.zBTtmb')
#     # This is getting all flight results
#     category_results = parser.root.css('.Rk10dc')

#     for category, category_result in zip(categories, category_results):
#         # This is going to hold data for each category
#         category_data = []

#         # This is iterating through each flight result
#         for result in category_result.css('.yR1fYc'):
#             date_elements = result.css('[jscontroller="cNtv4b"] span')
#             departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
#             arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
#             company = result.css_first('.Ir0Voe .sSHqwe').text() # This is getting airline name
#             duration = result.css_first('.AdWm1c.gvkrdb').text() # This is getting flight duration
#             stops = result.css_first('.EfT7Ae .ogfYpf').text() # This is getting the number of stops
#             emissions = result.css_first('.V1iAHe .AdWm1c').text() # This is getting emissions data
#             emission_comparison = result.css_first('.N6PNV').text() # This is getting emission comparison data
#             price = result.css_first('.U3gSDe .FpEdX span').text() # This is getting the price
#             price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None # This is getting different price types if it is available

#         # Assuming return_result represents a flight result element from which we are extracting data

#             # This is getting the container div for the airline info
#             airline_container = result.css_first('.sSHqwe.tPgKwe.ogfYpf')

#             # Initialize an empty list to store airline names
#             airline_names = []

#             # This is iterating through each span element inside the container
#             for span in airline_container.css('span'):
#                 # Extract the text content from the span element
#                 span_text = span.text().strip()
                
#                 # Filter out unwanted text
#                 if 'Operated by' not in span_text and not span.attrs:
#                     # Add the valid airline name to the list
#                     airline_names.append(span_text)

#             # Join all collected airline names with a comma
#             airline_names_str = ', '.join(airline_names)

#             # This is going to hold flight data
#             flight_data = {
#                 'departure_date': departure_date,
#                 'arrival_date': arrival_date,
#                 'company': airline_names_str,  # Use the extracted airline names
#                 'duration': duration,
#                 'stops': stops,
#                 'emissions': emissions,
#                 'emission_comparison': emission_comparison,
#                 'price': price,
#                 'price_type': price_type
#             }

#             # This is getting airport information
#             airports = result.css_first('.Ak5kof .sSHqwe')
#             service = result.css_first('.hRBhge')

#             # If service data is available, it will be added to flight data
#             if service:
#                 flight_data['service'] = service.text()
#             else:
#                 flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text() # This is getting departure airport from the user
#                 flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text() # This is getting arrival airport from the user

#             # Adding the code to scrape stop duration and location
#             stop_info = result.css('.sSHqwe.tPgKwe.ogfYpf')
#             stops_data = []

#             for stop in stop_info:
#                 # Extracting stop duration and location from aria-label
#                 stop_details = stop.attrs.get('aria-label', '')
#                 layovers = stop_details.split('Layover')

#                 for layover in layovers[1:]:  # Skip the first split part as it's empty
#                     parts = layover.split(' is a ')
#                     if len(parts) > 1:
#                         # Further split to get duration and location separately
#                         duration_and_location = parts[1].split(' layover at ')
#                         if len(duration_and_location) == 2:
#                             stop_duration = duration_and_location[0].strip()
#                             location_info = duration_and_location[1].strip()
#                             # Extract full stop location
#                             stop_location = location_info.split(' in ')[0] if ' in ' in location_info else location_info

#                             stop_data = {
#                                 'stop_duration': stop_duration,
#                                 'stop_location': stop_location
#                             }
#                             stops_data.append(stop_data)
                    
#             flight_data['stops_data'] = stops_data

#             # This is adding flight data to category
#             category_data.append(flight_data)

#         # This is adding the category data to the main dictionary
#         data[category.text().lower().replace(' ', '_')] = category_data

    
#     if parser_return:
#         # This is getting all return flight categories
#         return_categories = parser_return.root.css('.zBTtmb')
#         # This is getting all return flight results
#         return_category_results = parser_return.root.css('.Rk10dc')

#         for return_category, return_category_result in zip(return_categories, return_category_results):
#             # This is going to hold data for each return category
#             return_category_data = []

#             # This is iterating through each return flight result
#             for return_result in return_category_result.css('.yR1fYc'):
#                 date_elements = return_result.css('[jscontroller="cNtv4b"] span') # This is finding date information
#                 departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
#                 arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
#                 company = return_result.css_first('.Ir0Voe .sSHqwe').text() # This is getting airline name
#                 duration = return_result.css_first('.AdWm1c.gvkrdb').text() # This is getting flight duration
#                 stops = return_result.css_first('.EfT7Ae .ogfYpf').text() # This is getting the number of stops
#                 emissions = return_result.css_first('.V1iAHe .AdWm1c').text() # This is getting emissions data
#                 emission_comparison = return_result.css_first('.N6PNV').text() # This is getting emission comparison data
#                 price = return_result.css_first('.U3gSDe .FpEdX span').text() # This is getting the price
#                 price_type = return_result.css_first('.U3gSDe .N872Rd').text() if return_result.css_first('.U3gSDe .N872Rd') else None # This is getting different price types if it is available

#                 # Assuming return_result represents a flight result element from which we are extracting data

#                 # This is getting the container div for the airline info
#                 airline_container = return_result.css_first('.sSHqwe.tPgKwe.ogfYpf')

#                 # This is getting the last span element inside the container, which contains the airline names
#                 last_span_element = airline_container.css('span')[-1]

#                 # Extracting the text content from the span element
#                 airline_names = last_span_element.text().strip()

#                 # This is going to hold flight data
#                 return_flight_data = {
#                     'departure_date': departure_date,
#                     'arrival_date': arrival_date,
#                     'company': airline_names,  # Use the extracted airline names
#                     'duration': duration,
#                     'stops': stops,
#                     'emissions': emissions,
#                     'emission_comparison': emission_comparison,
#                     'price': price,
#                     'price_type': price_type
#                 }

#                 # This is getting airport information
#                 airports = return_result.css_first('.Ak5kof .sSHqwe')
#                 service = return_result.css_first('.hRBhge')


#                 # If service data is available, it will be added to flight data
#                 if service:
#                     return_flight_data['service'] = service.text()
#                 else:
#                     return_flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text() # This is getting departure airport from the user
#                     return_flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text() # This is getting arrival airport from the user

#                 # This is adding return flight data to return category
#                 return_category_data.append(return_flight_data)

#                 # Adding the code to scrape stop duration and location for return flights
#                 stop_info = return_result.css('.sSHqwe.tPgKwe.ogfYpf')
#                 stops_data = []

#                 for stop in stop_info:
#                     # Extracting stop duration and location from aria-label
#                     stop_details = stop.attrs.get('aria-label', '')
#                     layovers = stop_details.split('Layover')

#                     for layover in layovers[1:]:  # Skip the first split part as it's empty
#                         parts = layover.split(' is a ')
#                         if len(parts) > 1:
#                             # Further split to get duration and location separately
#                             duration_and_location = parts[1].split(' layover at ')
#                             if len(duration_and_location) == 2:
#                                 stop_duration = duration_and_location[0].strip()
#                                 location_info = duration_and_location[1].strip()
#                                 # Extract full stop location
#                                 stop_location = location_info.split(' in ')[0] if ' in ' in location_info else location_info

#                                 stop_data = {
#                                     'stop_duration': stop_duration,
#                                     'stop_location': stop_location
#                                 }
#                                 stops_data.append(stop_data)

#                 return_flight_data['stops_data'] = stops_data

#             # This is adding the return category data to the main dictionary
#             data[f'return_{return_category.text().lower().replace(" ", "_")}'] = return_category_data

#     return data

# def main():
#     # This is going to take user input
#     from_place = input("Enter the departure location: ")
#     to_place = input("Enter the destination: ")
#     departure_date = input("Enter the departure date (YYYY-MM-DD): ")
#     trip_type = input("Enter the trip type (Round Trip or One Way): ")
#     seat_type = input("Enter the seat type (Economy, Business, First class): ")
#     return_date = ''
#     if trip_type.lower() == 'round trip':
#         return_date = input("Enter the return date (YYYY-MM-DD): ")

#     with sync_playwright() as playwright:
#         parser, parser_return = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
#         flight_data = scrape_google_flights(parser, parser_return)
#         print(json.dumps(flight_data, indent=4))

# if __name__ == '__main__':
#     main()








# from playwright.sync_api import sync_playwright
# from selectolax.lexbor import LexborHTMLParser
# import json
# import time

# # Function to enter user input into Google Flights and scrape flights data
# def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
#     browser = playwright.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

#     # Select trip type (Round Trip or One Way)
#     trip_type_menu = page.query_selector('.VfPpkd-aPP78e')
#     if trip_type_menu:
#         trip_type_menu.click()
#         time.sleep(1)
#         trip_type_options = page.query_selector_all('li[role="option"]')
#         for option in trip_type_options:
#             option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#             if trip_type.lower() in option_text.lower():
#                 option.click()
#                 break
#         time.sleep(1)
#     else:
#         print("Trip type menu not found")

#     # Select seat type (Economy, Business, First class)
#     seat_type_menu = page.query_selector('.JQrP8b')
#     if seat_type_menu:
#         seat_type_menu.click()
#         time.sleep(1)
#         seat_type_options = page.query_selector_all('li[role="option"]')
#         for option in seat_type_options:
#             option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#             if seat_type.lower() in option_text.lower():
#                 option.click()
#                 break
#         time.sleep(1)
#     else:
#         print("Seat type menu not found")

#     # Enter "From" location
#     from_place_field = page.query_selector_all('.e5F5td')[0]
#     from_place_field.click()
#     time.sleep(1)
#     from_place_field.type(from_place)
#     time.sleep(1)
#     page.keyboard.press('Enter')

#     # Enter "To" location
#     to_place_field = page.query_selector_all('.e5F5td')[1]
#     to_place_field.click()
#     time.sleep(1)
#     to_place_field.type(to_place)
#     time.sleep(1)
#     page.keyboard.press('Enter')

#     # Enter departure date
#     departure_date_field = page.query_selector('[aria-label="Departure"]')
#     if departure_date_field:
#         departure_date_field.click()
#         time.sleep(1)
#         page.keyboard.type(departure_date)
#         time.sleep(1)
#         page.keyboard.press('Tab')  # Move to the return date field if round trip
#     else:
#         print("Departure date field not found")

#     if trip_type.lower() == 'round trip':
#         # Enter return date
#         time.sleep(1)
#         page.keyboard.type(return_date)
#         time.sleep(1)

#         # Click done button
#         done_button = page.query_selector('button[jsname="McfNlf"][aria-label^="Done"]')
#         if done_button:
#             done_button.click()
#         else:
#             print("Done button not found")

#     time.sleep(2)  # Wait for the date picker to close

#     time.sleep(5)  # Wait for results to load

#     # Scroll to load more results
#     for _ in range(3):
#         page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
#         time.sleep(2)

#     # Parse the page for data
#     parser = LexborHTMLParser(page.content())

#     if trip_type.lower() == 'round trip':
#         # Scrape the initial URL to navigate back to this page later
#         initial_url = page.url

#         # Get all departing flights
#         departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')

#         return_flight_data = []
#         for departing_flight in departing_flights:
#             departing_flight.click()
#             time.sleep(5)

#             # Scrape return flights after selecting a departing flight
#             parser_return = LexborHTMLParser(page.content())
#             return_flight_data = scrape_google_flights(parser, parser_return)

#             # Navigate back to the initial departing flights list
#             page.goto(initial_url)
#             time.sleep(5)

#         # Close browser after processing all flights
#         browser.close()
#         return return_flight_data
#     else:
#         browser.close()
#         return scrape_google_flights(parser)

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
#     from_place = input("Enter departure location: ")
#     to_place = input("Enter destination location: ")
#     departure_date = input("Enter departure date (e.g., 2024-09-10): ")
#     return_date = input("Enter return date (e.g., 2024-09-15): ")
#     trip_type = input("Enter trip type (Round Trip or One Way): ")
#     seat_type = input("Enter seat type (Economy, Business, First class): ")

#     with sync_playwright() as playwright:
#         if trip_type.lower() == 'round trip':
#             parser, return_flight_data = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
#             data = scrape_google_flights(parser, parser_return=return_flight_data)
#         else:
#             parser, _ = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
#             data = scrape_google_flights(parser)

#         print(json.dumps(data, indent=4))

# if __name__ == "__main__":
#     main()





from playwright.sync_api import sync_playwright
# from selectolax.lexbor import LexborHTMLParser
# import json
# import time

# # This function is going to enter the information the user passes as input into Google Flights
# def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
#     # This is creating a new browser instance
#     browser = playwright.chromium.launch(headless=False)
#     # This is opening a chrome page
#     page = browser.new_page()
#     # This is the page that is being scraped
#     page.goto('https://www.google.com/travel/flights/search?tfs=CBwQAhokEgoyMDI0LTA4LTE0ag0IAhIJL20vMDJfMjg2cgcIARIDTEFYGiQSCjIwMjQtMDgtMzFqBwgBEgNMQVhyDQgCEgkvbS8wMl8yODZAAUgBcAGCAQsI____________AZgBAQ&hl=en-US&gl=US')

#     # Select trip type (Round Trip or One Way)
#     trip_type_menu = page.query_selector('.VfPpkd-aPP78e')
#     if trip_type_menu:
#         trip_type_menu.click()
#         time.sleep(1)
#         trip_type_options = page.query_selector_all('li[role="option"]')
#         for option in trip_type_options:
#             option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#             if trip_type.lower() in option_text.lower():
#                 option.click()
#                 break
#         time.sleep(1)
#     else:
#         print("Trip type menu not found")

#     # Select seat type (Economy, Business, First class)
#     seat_type_menu = page.query_selector('.JQrP8b')
#     if seat_type_menu:
#         seat_type_menu.click()
#         time.sleep(1)
#         seat_type_options = page.query_selector_all('li[role="option"]')
#         for option in seat_type_options:
#             option_text = option.query_selector('.VfPpkd-rymPhb-fpDzbe-fmcmS').text_content()
#             print(f"Seat type option found: {option_text}")
#             if seat_type.lower() in option_text.lower():
#                 option.click()
#                 print(f"seat_type = '{seat_type}'")
#                 break
#         time.sleep(1)
#     else:
#         print("Seat type menu not found")

#     # This is filling up From field
#     from_place_field = page.query_selector_all('.e5F5td')[0] # .e5F5td is the From div
#     from_place_field.click()
#     time.sleep(1)
#     from_place_field.type(from_place) # This is entering where we are traveling from
#     time.sleep(1)
#     page.keyboard.press('Enter')

#     # This is filling up To field
#     to_place_field = page.query_selector_all('.e5F5td')[1] # .e5F5td is the To div
#     to_place_field.click()
#     time.sleep(1)
#     to_place_field.type(to_place) # This is entering where we are going to
#     time.sleep(1)
#     page.keyboard.press('Enter')

#     # This is filling up Departure Date
#     departure_date_field = page.query_selector('[aria-label="Departure"]') # [aria-label="Departure"] this is the departure date field
#     if departure_date_field:
#         departure_date_field.click()
#         time.sleep(1)
#         page.keyboard.type(departure_date) # This is entering Departure Date
#         time.sleep(1)
#         page.keyboard.press('Tab')  # Move to the return date field if round trip
#     else:
#         print("Departure date field not found")

#     if trip_type.lower() == 'round trip':
#         # This is filling up Return Date
#         time.sleep(1)
#         page.keyboard.type(return_date) # This is entering Return Date
#         time.sleep(1)

#         # Once Departure and Return dates are filled, the done button will be pressed
#         done_button = page.query_selector('button[jsname="McfNlf"][aria-label^="Done"]') # This is finding the done button
#         if done_button:
#             done_button.click()
#         else:
#             print("Done button not found")

#     time.sleep(2)  # Wait for the date picker to close

#     time.sleep(5)  # Wait for results to load

#     # This is going to scroll to the bottom of the page so more results can be loaded
#     for _ in range(3):
#         page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
#         time.sleep(2)

#         # This is going to parse the page using Selectolax for the data that we are looking for
#         parser = LexborHTMLParser(page.content())

#         if trip_type.lower() == 'round trip':
#             # Locate the element representing the first flight (departure) and click on it to reveal return flights
#             first_flight_selector = '.yR1fYc[jsaction*="click:O1htCb"]'
#             first_flight = page.query_selector(first_flight_selector)

#             if first_flight:
#                 first_flight.click()
#                 # Wait for the return flight options to load
#                 time.sleep(5)

#                 # Capture the dynamically generated URL for the return flight page
#                 return_flight_url = page.url  # Capture the dynamically generated URL

#                 # print(f"Return flight URL: {return_flight_url}")  # Optional: For debugging

#                 # Parse the return flight data
#                 parser_return = LexborHTMLParser(page.content())

#                 # After the data is parsed, the browser will be closed
#                 browser.close()

#                 # This is returning both the parsed data from the website
#                 return parser, parser_return
#             else:
#                 print("No departure flight found.")
#                 browser.close()
#                 return parser, None
#         else:
#             # After the data is parsed, the browser will be closed
#             browser.close()

#             # This is returning the parsed data from the website
#             return parser, None
# # This function is going to parse and scrape data from Google Flights and store it in a dictionary
# def scrape_google_flights(parser, parser_return=None):
#     # This dictionary is going to hold the scraped data
#     data = {}

#     # This is getting all flight categories
#     categories = parser.root.css('.zBTtmb')
#     # This is getting all flight results
#     category_results = parser.root.css('.Rk10dc')

#     for category, category_result in zip(categories, category_results):
#         # This is going to hold data for each category
#         category_data = []

#         # This is iterating through each flight result
#         for result in category_result.css('.yR1fYc'):
#             date_elements = result.css('[jscontroller="cNtv4b"] span')
#             departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
#             arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
#             company = result.css_first('.Ir0Voe .sSHqwe').text() # This is getting airline name
#             duration = result.css_first('.AdWm1c.gvkrdb').text() # This is getting flight duration
#             stops = result.css_first('.EfT7Ae .ogfYpf').text() # This is getting the number of stops
#             emissions = result.css_first('.V1iAHe .AdWm1c').text() # This is getting emissions data
#             emission_comparison = result.css_first('.N6PNV').text() # This is getting emission comparison data
#             price = result.css_first('.U3gSDe .FpEdX span').text() # This is getting the price
#             price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None # This is getting different price types if it is available

#         # Assuming return_result represents a flight result element from which we are extracting data

#             # This is getting the container div for the airline info
#             airline_container = result.css_first('.sSHqwe.tPgKwe.ogfYpf')

#             # Initialize an empty list to store airline names
#             airline_names = []

#             # This is iterating through each span element inside the container
#             for span in airline_container.css('span'):
#                 # Extract the text content from the span element
#                 span_text = span.text().strip()
                
#                 # Filter out unwanted text
#                 if 'Operated by' not in span_text and not span.attrs:
#                     # Add the valid airline name to the list
#                     airline_names.append(span_text)

#             # Join all collected airline names with a comma
#             airline_names_str = ', '.join(airline_names)

#             # This is going to hold flight data
#             flight_data = {
#                 'departure_date': departure_date,
#                 'arrival_date': arrival_date,
#                 'company': airline_names_str,  # Use the extracted airline names
#                 'duration': duration,
#                 'stops': stops,
#                 'emissions': emissions,
#                 'emission_comparison': emission_comparison,
#                 'price': price,
#                 'price_type': price_type
#             }

#             # This is getting airport information
#             airports = result.css_first('.Ak5kof .sSHqwe')
#             service = result.css_first('.hRBhge')

#             # If service data is available, it will be added to flight data
#             if service:
#                 flight_data['service'] = service.text()
#             else:
#                 flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text() # This is getting departure airport from the user
#                 flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text() # This is getting arrival airport from the user

#             # Adding the code to scrape stop duration and location
#             stop_info = result.css('.sSHqwe.tPgKwe.ogfYpf')
#             stops_data = []

#             for stop in stop_info:
#                 # Extracting stop duration and location from aria-label
#                 stop_details = stop.attrs.get('aria-label', '')
#                 layovers = stop_details.split('Layover')

#                 for layover in layovers[1:]:  # Skip the first split part as it's empty
#                     parts = layover.split(' is a ')
#                     if len(parts) > 1:
#                         # Further split to get duration and location separately
#                         duration_and_location = parts[1].split(' layover at ')
#                         if len(duration_and_location) == 2:
#                             stop_duration = duration_and_location[0].strip()
#                             location_info = duration_and_location[1].strip()
#                             # Extract full stop location
#                             stop_location = location_info.split(' in ')[0] if ' in ' in location_info else location_info

#                             stop_data = {
#                                 'stop_duration': stop_duration,
#                                 'stop_location': stop_location
#                             }
#                             stops_data.append(stop_data)
                    
#             flight_data['stops_data'] = stops_data

#             # This is adding flight data to category
#             category_data.append(flight_data)

#         # This is adding the category data to the main dictionary
#         data[category.text().lower().replace(' ', '_')] = category_data

    
#     if parser_return:
#         # This is getting all return flight categories
#         return_categories = parser_return.root.css('.zBTtmb')
#         # This is getting all return flight results
#         return_category_results = parser_return.root.css('.Rk10dc')

#         for return_category, return_category_result in zip(return_categories, return_category_results):
#             # This is going to hold data for each return category
#             return_category_data = []

#             # This is iterating through each return flight result
#             for return_result in return_category_result.css('.yR1fYc'):
#                 date_elements = return_result.css('[jscontroller="cNtv4b"] span') # This is finding date information
#                 departure_date = date_elements[0].text().replace('\u202f', ' ').replace(' ', '').strip()
#                 arrival_date = date_elements[1].text().replace('\u202f', ' ').replace(' ', '').replace('+1', '').strip()
#                 company = return_result.css_first('.Ir0Voe .sSHqwe').text() # This is getting airline name
#                 duration = return_result.css_first('.AdWm1c.gvkrdb').text() # This is getting flight duration
#                 stops = return_result.css_first('.EfT7Ae .ogfYpf').text() # This is getting the number of stops
#                 emissions = return_result.css_first('.V1iAHe .AdWm1c').text() # This is getting emissions data
#                 emission_comparison = return_result.css_first('.N6PNV').text() # This is getting emission comparison data
#                 price = return_result.css_first('.U3gSDe .FpEdX span').text() # This is getting the price
#                 price_type = return_result.css_first('.U3gSDe .N872Rd').text() if return_result.css_first('.U3gSDe .N872Rd') else None # This is getting different price types if it is available

#                 # Assuming return_result represents a flight result element from which we are extracting data

#                 # This is getting the container div for the airline info
#                 airline_container = return_result.css_first('.sSHqwe.tPgKwe.ogfYpf')

#                 # This is getting the last span element inside the container, which contains the airline names
#                 last_span_element = airline_container.css('span')[-1]

#                 # Extracting the text content from the span element
#                 airline_names = last_span_element.text().strip()

#                 # This is going to hold flight data
#                 return_flight_data = {
#                     'departure_date': departure_date,
#                     'arrival_date': arrival_date,
#                     'company': airline_names,  # Use the extracted airline names
#                     'duration': duration,
#                     'stops': stops,
#                     'emissions': emissions,
#                     'emission_comparison': emission_comparison,
#                     'price': price,
#                     'price_type': price_type
#                 }

#                 # This is getting airport information
#                 airports = return_result.css_first('.Ak5kof .sSHqwe')
#                 service = return_result.css_first('.hRBhge')


#                 # If service data is available, it will be added to flight data
#                 if service:
#                     return_flight_data['service'] = service.text()
#                 else:
#                     return_flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text() # This is getting departure airport from the user
#                     return_flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text() # This is getting arrival airport from the user

#                 # This is adding return flight data to return category
#                 return_category_data.append(return_flight_data)

#                 # Adding the code to scrape stop duration and location for return flights
#                 stop_info = return_result.css('.sSHqwe.tPgKwe.ogfYpf')
#                 stops_data = []

#                 for stop in stop_info:
#                     # Extracting stop duration and location from aria-label
#                     stop_details = stop.attrs.get('aria-label', '')
#                     layovers = stop_details.split('Layover')

#                     for layover in layovers[1:]:  # Skip the first split part as it's empty
#                         parts = layover.split(' is a ')
#                         if len(parts) > 1:
#                             # Further split to get duration and location separately
#                             duration_and_location = parts[1].split(' layover at ')
#                             if len(duration_and_location) == 2:
#                                 stop_duration = duration_and_location[0].strip()
#                                 location_info = duration_and_location[1].strip()
#                                 # Extract full stop location
#                                 stop_location = location_info.split(' in ')[0] if ' in ' in location_info else location_info

#                                 stop_data = {
#                                     'stop_duration': stop_duration,
#                                     'stop_location': stop_location
#                                 }
#                                 stops_data.append(stop_data)

#                 return_flight_data['stops_data'] = stops_data

#             # This is adding the return category data to the main dictionary
#             data[f'return_{return_category.text().lower().replace(" ", "_")}'] = return_category_data

#     return data

# def main():
#     # This is going to take user input
#     from_place = input("Enter the departure location: ")
#     to_place = input("Enter the destination: ")
#     departure_date = input("Enter the departure date (YYYY-MM-DD): ")
#     trip_type = input("Enter the trip type (Round Trip or One Way): ")
#     seat_type = input("Enter the seat type (Economy, Business, First class): ")
#     return_date = ''
#     if trip_type.lower() == 'round trip':
#         return_date = input("Enter the return date (YYYY-MM-DD): ")

#     with sync_playwright() as playwright:
#         parser, parser_return = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
#         flight_data = scrape_google_flights(parser, parser_return)
#         print(json.dumps(flight_data, indent=4))

# if __name__ == '__main__':
#     main()




from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import json
import time

# Function to enter user input into Google Flights and scrape flights data
def get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
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
            if seat_type.lower() in option_text.lower():
                option.click()
                break
        time.sleep(1)
    else:
        print("Seat type menu not found")

    # Enter "From" location
    from_place_field = page.query_selector_all('.e5F5td')[0]
    from_place_field.click()
    time.sleep(1)
    from_place_field.type(from_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # Enter "To" location
    to_place_field = page.query_selector_all('.e5F5td')[1]
    to_place_field.click()
    time.sleep(1)
    to_place_field.type(to_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # Enter departure date
    departure_date_field = page.query_selector('[aria-label="Departure"]')
    if departure_date_field:
        departure_date_field.click()
        time.sleep(1)
        page.keyboard.type(departure_date)
        time.sleep(1)
        page.keyboard.press('Tab')  # Move to the return date field if round trip
    else:
        print("Departure date field not found")

    if trip_type.lower() == 'round trip':
        # Enter return date
        time.sleep(1)
        page.keyboard.type(return_date)
        time.sleep(1)

        # Click done button
        done_button = page.query_selector('button[jsname="McfNlf"][aria-label^="Done"]')
        if done_button:
            done_button.click()
        else:
            print("Done button not found")

    time.sleep(2)  # Wait for the date picker to close

    time.sleep(5)  # Wait for results to load

    for _ in range(3):
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)

    parser_departing = LexborHTMLParser(page.content())
    all_departing_flights_data = scrape_google_flights(parser_departing)

    # Get all departing flight elements
    departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')

    max_flights_to_scrape = 5  # Set the desired limit here
    all_flight_data = []

    # Scrape the initial URL to navigate back to this page later
    initial_url = page.url

    # Determine the key for departing flights in the scraped data
    departing_key = next(iter(all_departing_flights_data.keys()))

    # Determine the number of flights to actually scrape
    num_flights_to_scrape = min(len(departing_flights), len(all_departing_flights_data[departing_key]), max_flights_to_scrape)

    for index in range(num_flights_to_scrape):
        # Get the departing flight data for this index
        departing_flight_data = all_departing_flights_data[departing_key][index]

        # Check if the corresponding element still exists
        if index < len(departing_flights):
            # Click on the departing flight
            departing_flights[index].click()
            time.sleep(5)

            # Scrape return flights after selecting a departing flight
            parser_return = LexborHTMLParser(page.content())
            return_flight_data = scrape_google_flights(parser_return)
            
            # Combine departing and return flight data
            combined_data = {
                'departing_flight': departing_flight_data,
                'return_flights': return_flight_data,
                'departing_flight_index': index
            }
            
            all_flight_data.append(combined_data)

            # Navigate back to the initial departing flights list
            page.goto(initial_url)
            time.sleep(5)

            # Re-select all departing flights without re-scraping
            departing_flights = page.query_selector_all('.yR1fYc[jsaction*="click:O1htCb"]')
        else:
            print(f"Warning: Flight element at index {index} no longer exists on the page.")

    # Close browser after processing all flights
    browser.close()
    return all_flight_data

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
        if trip_type.lower() == 'round trip':
            all_flight_data = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
            for index, flight_data in enumerate(all_flight_data):
                print(f"\nDeparting Flight {index + 1}:")
                print(json.dumps(flight_data, indent=4))
        else:
            parser, _ = get_page(playwright, from_place, to_place, departure_date, return_date, trip_type, seat_type)
            data = scrape_google_flights(parser)
            print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()


