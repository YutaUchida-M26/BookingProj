## Django Hotel Booking Application

This is a simple Django hotel booking application that allows users to search for hotels, view available rooms, and make reservations. Below is a brief explanation of each functionality in the application:

### Functionality

1. **Top Page (`topPage`)**:
   - This is the landing page of the application.
   - Users are redirected to this page when they log out from the system.
   - It provides a welcoming interface with options to explore further.

2. **Search Page (`searchPage`)**:
   - This page allows users to search for hotels based on certain criteria.
   - It displays a form where users can select a city, room type, check-in date, and check-out date.
   - The form includes a date picker to ensure proper date selection.
   - The available search options include cities, room types, and dates within the next two weeks from the current date.

3. **Hotel List (`hotelList`)**:
   - This page displays a list of hotels and their available rooms based on the search criteria from the search page.
   - When the user submits the search form, it queries the database for available hotels and rooms that match the specified criteria.
   - The system checks the availability of rooms for consecutive dates to ensure users can book multiple nights if needed.
   - Hotels with zero available rooms are not displayed in the list.
   - Error and success messages from the reservation process are shown on this page.

4. **Reservation (`reservation`)**:
   - This page allows users to make a reservation for a specific hotel and room type.
   - Users can select the check-in and check-out dates for their reservation.
   - The system checks the availability of rooms for the selected dates to ensure a valid reservation.
   - If the reservation is successful, the room count for the selected dates is reduced by one.
   - If the room count becomes zero for any date during the selected stay, the reservation fails.
   - Users must be logged in to make a reservation, but if not logged in, they are prompted to create a new user account.

5. **Login (`login_user`)**:
   - This page provides a form for users to log into the system.
   - Users need to provide their username and password to log in.
   - If the login is successful, the user is redirected to the top page.
   - If the login fails, an appropriate error message is displayed.

6. **Logout (`logout_user`)**:
   - This function logs out the currently logged-in user and redirects them to the top page.

7. **My Page (`my_page`)**:
   - This page displays the reservations made by the logged-in user.
   - If the user is not logged in, they are redirected to the login page.

### Models

The application uses the following Django models:

- `City`: Represents a city where hotels are located.
- `RoomType`: Represents types of rooms available in hotels (e.g., single, double, suite).
- `Hotel`: Represents a hotel with its name, location, etc.
- `HotelAvailability`: Represents the availability of rooms in hotels for specific dates.
- `Reservation`: Represents a user's reservation with details like the hotel, room type, check-in, and check-out dates.

Note: The actual model fields and their relationships are not detailed in the provided code but are essential for the application to function correctly.

This Django hotel booking application provides a straightforward way for users to search for hotels and make reservations. Further improvements and additional features can be added based on specific business requirements.
