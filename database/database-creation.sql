/* Query to Create Database */
​
GO
CREATE DATABASE AroundTheWorld;
GO
​
/* Query to use the created Database */
​
USE AroundTheWorld;
​
/* Query to Create Customer Entity */
​
CREATE TABLE Customer
(
CustID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
CustFirstName VARCHAR(50) NOT NULL,
CustLastName VARCHAR(50) NOT NULL,
CustBirthDate DATE NOT NULL,
CustPhoneNo INT NOT NULL,
CustStreetName VARCHAR(50) NOT NULL,
CustZipCode VARCHAR(10) NOT NULL,
CustEmail VARCHAR(50) NOT NULL,
CustPassword VARCHAR(50) NOT NULL,
CustAge INT NOT NULL,
CustGender VARCHAR(10) NOT NULL
);
​
/* Query to Create Employee Entity */
​
CREATE TABLE Employee
(
EmployeeID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
EmpFirstName VARCHAR(50) NOT NULL,
EmpLastName VARCHAR(50) NOT NULL,
EmpPhoneNumber INT NOT NULL,
EmpEmailAddress VARCHAR(50) NOT NULL,
EmpUsername VARCHAR(50) NOT NULL,
EmpPassword VARCHAR(50) NOT NULL,
EmpDesignation VARCHAR(50) NOT NULL,
EmpSalary FLOAT NOT NULL,
EmpAvgRating INT
);
​
/* Query to Create CustomerPreference Entity */
​
CREATE TABLE CustomerPreference
(
CustPrefID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
CustID INT NOT NULL FOREIGN KEY REFERENCES Customer(CustID),
CustBudget FLOAT NOT NULL,
PrefPackageType VARCHAR(50) NOT NULL
);
​
/* Query to Create Country Entity */
​
CREATE TABLE Country
(
CountryID INT PRIMARY KEY IDENTITY(1, 1),
CountryName VARCHAR(50) NOT NULL
);
​
/* Query to Create Visa Entity */
​
CREATE TABLE Visa
(
VisaID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
CountryID INT NOT NULL FOREIGN KEY REFERENCES Country(CountryID),
IsVisaRequired BIT NOT NULL,
VisaCost FLOAT
);
​
/* Query to Create VisaStatus Entity */
​
CREATE TABLE VisaStatus
(
VisaStatusID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
CustID INT NOT NULL FOREIGN KEY REFERENCES Customer(CustID),
VisaID INT NOT NULL FOREIGN KEY REFERENCES Visa(VisaID),
VisaOutcome VARCHAR(50) NOT NULL,
RejectedReason VARCHAR(255),
VisaDate DATETIME NOT NULL DEFAULT GETDATE()
);
​
/* Query to Create Package Entity */
​
CREATE TABLE Package
(
PackageID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
PackageType VARCHAR(50) NOT NULL,
TotalPackagePrice FLOAT NOT NULL,
TotalNumberOfDays INT NOT NULL,
);
​
/* Query to Create Booking Entity */
​
CREATE TABLE Booking
(
BookingID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
PackageID INT NOT NULL FOREIGN KEY REFERENCES Package(PackageID),
EmployeeID INT NOT NULL FOREIGN KEY REFERENCES Employee(EmployeeID),
CustID INT NOT NULL FOREIGN KEY REFERENCES Customer(CustID),
IsLatest BIT NOT NULL,
BookingStatus VARCHAR(15) NOT NULL,
TripStartDate DATETIME NOT NULL DEFAULT GETDATE(),
TripEndDate DATETIME NOT NULL DEFAULT GETDATE(),
FinalBookingAmount FLOAT NOT NULL
);
​
/* Query to Create Payment Entity */
​
CREATE TABLE Payment
(
PaymentID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
BookingID INT NOT NULL FOREIGN KEY REFERENCES Booking(BookingID),
Discount FLOAT,
FinalAmount FLOAT NOT NULL,
PaymentStatus BIT NOT NULL,
PaymentMode VARCHAR(50) NOT NULL,
PaymentDate DATETIME NOT NULL DEFAULT GETDATE()
);
​
/* Query to Create CustomerFeedback Entity */
​
CREATE TABLE CustomerFeedback
(
BookingID INT NOT NULL FOREIGN KEY REFERENCES Booking(BookingID),
CustomerRating INT,
FeedbackDescription VARCHAR(255)
CONSTRAINT PKCustomerFeedback PRIMARY KEY CLUSTERED
(BookingID)
);
​
/* Query to Create City Entity */
​
CREATE TABLE City
(
CityID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
CountryID INT NOT NULL FOREIGN KEY REFERENCES Country(CountryID),
CityName VARCHAR(50) NOT NULL
);
​
/* Query to Create CustPreferredCity Entity */
​
CREATE TABLE CustPreferredCity 
(
CustPrefID INT NOT NULL FOREIGN KEY REFERENCES CustomerPreference(CustPrefID),
CityID INT NOT NULL FOREIGN KEY REFERENCES City(CityID)
CONSTRAINT PKCustPreferredCity PRIMARY KEY CLUSTERED
(CustPrefID, CityID)
);
​
/* Query to Create Transport Entity */
​
CREATE TABLE Transport
(
TransportID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
ArrivalCityID INT NOT NULL FOREIGN KEY REFERENCES City(CityID),
DepartureCityID INT NOT NULL FOREIGN KEY REFERENCES City(CityID),
TravelMode VARCHAR(50) NOT NULL,
TransportPrice FLOAT NOT NULL,
ArrivalDateAndTime DATETIME NOT NULL DEFAULT GETDATE(),
DepartureDateAndTime DATETIME NOT NULL DEFAULT GETDATE(),
Source VARCHAR(50) NOT NULL,
Destination VARCHAR(50) NOT NULL
);
​
/* Query to Create Attraction Entity */
​
CREATE TABLE Attraction
(
AttractionID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
AttractionName VARCHAR(50) NOT NULL,
AttractionPrice FLOAT NOT NULL
);
​
/* Query to Create Accommodation Entity */
​
CREATE TABLE Accommodation
(
AccommodationID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
AccommodationType VARCHAR(50) NOT NULL,
AccommodationName VARCHAR(50) NOT NULL,
AccommodationPrice FLOAT NOT NULL,
AccommodationRating INT NOT NULL,
AccommodationStreetName VARCHAR(50) NOT NULL,
AccommodationZipCode VARCHAR(10) NOT NULL
);
​
/* Query to Create PackageDetails Entity */
​
CREATE TABLE PackageDetails
(
PackageID INT NOT NULL FOREIGN KEY REFERENCES Package(PackageID),
AttractionID INT NOT NULL FOREIGN KEY REFERENCES Attraction(AttractionID),
AccommodationID INT NOT NULL FOREIGN KEY REFERENCES Accommodation(AccommodationID),
TransportID INT NOT NULL FOREIGN KEY REFERENCES Transport(TransportID),
CityID INT NOT NULL FOREIGN KEY REFERENCES City(CityID)
CONSTRAINT PKPackageDetails PRIMARY KEY CLUSTERED
(PackageID, AttractionID, AccommodationID, TransportID, CityID)
);
​
/* Query to Create Flight Entity */
​
CREATE TABLE Flight
(
TransportID INT NOT NULL FOREIGN KEY REFERENCES Transport(TransportID),
IsLatest BIT,
FlightPrice FLOAT,
LastUpdated DATETIME DEFAULT GETDATE()
CONSTRAINT PKFlight PRIMARY KEY CLUSTERED
(TransportID)
);
