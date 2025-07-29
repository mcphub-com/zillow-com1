import requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")
import aiohttp
from copy import deepcopy
import asyncio
import logging
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__rapidapi_url__ = 'https://rapidapi.com/apimaker/api/zillow-com1'

mcp = FastMCP('zillow-com1')

@mcp.tool()
def property_extended_search(location: Annotated[Union[str, None], Field(description='Location details (address, county, neighborhood or Zip code). It is required if the polygon or coordinates is empty. The maximum number of locations (city, zip code) is 5, separate location by ; Multi location /propertyExtendedSearch?location=78013;78014;New York, NY The maximum number of locations is 5 Max length: 100 Please note that for the ZIP Code Type PO Box there will be empty results.')] = None,
                             page: Annotated[Union[int, float, None], Field(description='Page number if at the previous response totalPages > 1. Max value is 20. To be able to access more data, you can break down your request by dividing it into price groups using the minPrice and maxPrice parameters. For example 0 - 100,000, 100,001 - 500,000, 500,001 - 800,000 and so on. This trick will help you to get more data. Default: 0')] = None,
                             status_type: Annotated[Literal['ForSale', 'ForRent', 'RecentlySold', None], Field(description='Valid values: ForSale, ForRent, RecentlySold')] = None,
                             home_type: Annotated[Union[str, None], Field(description='Property type comma-separated or empty for all types: For Rent Townhomes Houses Apartments_Condos_Co-ops For others: Multi-family Apartments Houses Manufactured Condos LotsLand Townhomes')] = None,
                             sort: Annotated[Union[str, None], Field(description='For status_type = ForSale OR RecentlySold are available: Homes_for_You Price_High_Low Price_Low_High Newest Bedrooms Bathrooms Square_Feet Lot_Size default Homes_for_You For status_type = ForRent are available: Verified_Source Payment_High_Low Payment_Low_High Newest Bedrooms Bathrooms Square_Feet Lot_Size default Verified_Source')] = None,
                             polygon: Annotated[Union[str, None], Field(description='Format: lon lat,lon1 lat1,lon2 lat2 It is required if the location or coordinates is empty. The last pair must be the same as the first pair.')] = None,
                             minPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForSale OR RecentlySold you can filter by min price. Default: 0')] = None,
                             maxPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForSale OR RecentlySold you can filter by max price. Default: 0')] = None,
                             rentMinPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForRent you can filter by min rent price. Default: 0')] = None,
                             rentMaxPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForRent you can filter by max rent price. Default: 0')] = None,
                             bathsMin: Annotated[Union[int, float, None], Field(description='Bathrooms min count Default: 0')] = None,
                             bathsMax: Annotated[Union[int, float, None], Field(description='Bathrooms max count Default: 0')] = None,
                             bedsMin: Annotated[Union[int, float, None], Field(description='Bedrooms min count Default: 0')] = None,
                             bedsMax: Annotated[Union[int, float, None], Field(description='Bedrooms max count Default: 0')] = None,
                             sqftMin: Annotated[Union[int, float, None], Field(description='Square Feet min value Default: 0')] = None,
                             sqftMax: Annotated[Union[int, float, None], Field(description='Square Feet max value. Default: 0')] = None,
                             buildYearMin: Annotated[Union[int, float, None], Field(description='Year Built min value. Default: 0')] = None,
                             buildYearMax: Annotated[Union[int, float, None], Field(description='Year Built max value. Default: 0')] = None,
                             daysOn: Annotated[Union[str, None], Field(description="Days on Z. Use with status_type='ForSale' or status_type='ForRent' Available values: 1,7,14,30,90,6m,12m,24m,36m")] = None,
                             soldInLast: Annotated[Union[str, None], Field(description="'Sold In Last' on Z. Use with status_type='RecentlySold'. Available values: 1,7,14,30,90,6m,12m,24m,36m")] = None,
                             isBasementFinished: Annotated[Union[int, float, None], Field(description='Basement filter. Set it to 1 if needed. Default: 0')] = None,
                             isBasementUnfinished: Annotated[Union[int, float, None], Field(description='Basement filter. Set it to 1 if needed. Default: 0')] = None,
                             isPendingUnderContract: Annotated[Union[int, float, None], Field(description='Pending & Under Contract filter. Set it to 1 if needed. Default: 0')] = None,
                             isAcceptingBackupOffers: Annotated[Union[int, float, None], Field(description='Accepting Backup Offers filter. Set it to 1 if needed. Default: 0')] = None,
                             isComingSoon: Annotated[Union[bool, None], Field(description='Coming Soon listings are homes that will soon be on the market.. Set it to 1 if needed.')] = None,
                             otherListings: Annotated[Union[bool, None], Field(description='If set to 1, the results will only include data from the Other Listings tab.')] = None,
                             isNewConstruction: Annotated[Union[bool, None], Field(description='New Construction filter. Set it to 1 or true if you only need properties with New Construction status.')] = None,
                             keywords: Annotated[Union[str, None], Field(description='Filter with keywords.')] = None,
                             lotSizeMin: Annotated[Union[str, None], Field(description='Available values: 1,000 sqft 2,000 sqft 3,000 sqft 4,000 sqft 5,000 sqft 7,500 sqft 1/4 acre/10,890 sqft 1/2 acre/21,780 sqft 1 acre/43,560 sqft')] = None,
                             lotSizeMax: Annotated[Union[str, None], Field(description='Available values: 1,000 sqft 2,000 sqft 3,000 sqft 4,000 sqft 5,000 sqft 7,500 sqft 1/4 acre/10,890 sqft 1/2 acre/21,780 sqft 1 acre/43,560 sqft 2 acres/87,120 sqft 5 acres/217,800 sqft 10 acres/435,600 sqft 20 acres/871,200 sqft 50 acres/2,178,000 sqft 100 acres/4,356,000 sqft')] = None,
                             saleByAgent: Annotated[Union[str, None], Field(description='Default - true. To get FSBO set saleByAgent=false&saleByOwner=true&otherListings=true.')] = None,
                             saleByOwner: Annotated[Union[str, None], Field(description='Default - true. To get only FSBO set saleByAgent=false&saleByOwner=true&otherListings=true')] = None,
                             isForSaleForeclosure: Annotated[Union[bool, None], Field(description='If you only need to get ForSaleForeclosure set to true or 1.')] = None,
                             isWaterfront: Annotated[Union[bool, None], Field(description='')] = None,
                             hasPool: Annotated[Union[bool, None], Field(description='')] = None,
                             hasAirConditioning: Annotated[Union[bool, None], Field(description='')] = None,
                             isCityView: Annotated[Union[bool, None], Field(description='')] = None,
                             isMountainView: Annotated[Union[bool, None], Field(description='')] = None,
                             isWaterView: Annotated[Union[bool, None], Field(description='')] = None,
                             isParkView: Annotated[Union[bool, None], Field(description='')] = None,
                             isOpenHousesOnly: Annotated[Union[bool, None], Field(description='Must have open house')] = None,
                             is3dHome: Annotated[Union[bool, None], Field(description='Must have 3D Tour')] = None,
                             coordinates: Annotated[Union[str, None], Field(description='It is required if the location or polygon is empty. Format: lon lat,diameter. Diameter in miles from 1 to 99 -118.51750373840332 34.007063913440916,20')] = None,
                             hoa: Annotated[Union[int, float, None], Field(description='Max HOA. Default: 0')] = None,
                             includeHomesWithNoHoaData: Annotated[Union[bool, None], Field(description='Default - true.')] = None,
                             isAuction: Annotated[Union[bool, None], Field(description='Auctions. Default true.')] = None,
                             schools: Annotated[Union[str, None], Field(description='Available values: elementary, public, private, middle, charter, high For multiple selection, separate with comma: middle,high')] = None,
                             schoolsRating: Annotated[Union[str, None], Field(description='Min school ratings. From 1 to 10')] = None,
                             includeUnratedSchools: Annotated[Union[bool, None], Field(description='Include schools with no rating')] = None,
                             hasGarage: Annotated[Union[bool, None], Field(description='Must have a garage. Default value false')] = None,
                             parkingSpots: Annotated[Union[int, float, None], Field(description='Parking Spots. Max value - 4 Default: 0')] = None,
                             isForeclosed: Annotated[Union[bool, None], Field(description='')] = None,
                             isPreForeclosure: Annotated[Union[bool, None], Field(description='')] = None,
                             isEntirePlace: Annotated[Union[bool, None], Field(description="Default - true. Apply when status_type = 'ForRent'. Set it to false if you need only a room.")] = None,
                             isRoom: Annotated[Union[bool, None], Field(description="Default - false. Apply when status_type = 'ForRent' Set it true and isEntirePlace to false if you need only a room.")] = None,
                             largeDogsAllowed: Annotated[Union[bool, None], Field(description='Allows large dogs. Only For Rent')] = None,
                             smallDogsAllowed: Annotated[Union[bool, None], Field(description='Allows small dogs. Only For Rent')] = None,
                             catsAllowed: Annotated[Union[bool, None], Field(description='Allows cats. Only For Rent')] = None,
                             noPets: Annotated[Union[bool, None], Field(description='No pets. Only For Rent')] = None,
                             moveInDate: Annotated[Union[str, datetime, None], Field(description='Move-in Date Only For Rent')] = None,
                             parkingAvailable: Annotated[Union[bool, None], Field(description='On-site Parking. Only For Rent')] = None,
                             inUnitLaundry: Annotated[Union[bool, None], Field(description='In-unit Laundry. Only For Rent')] = None,
                             acceptsApplications: Annotated[Union[bool, None], Field(description='Accepts Zillow Applications. Only For Rent')] = None,
                             incomeRestricted: Annotated[Union[bool, None], Field(description='Income restricted. Only For Rent')] = None,
                             hardwoodFloor: Annotated[Union[bool, None], Field(description='Hardwood Floors. Only For Rent')] = None,
                             disabledAccess: Annotated[Union[bool, None], Field(description='Disabled Access. Only For Rent')] = None,
                             utilitiesIncluded: Annotated[Union[bool, None], Field(description='Utilities Included. Only For Rent')] = None,
                             shortTermLease: Annotated[Union[bool, None], Field(description='Short term lease available. Only For Rent')] = None,
                             furnished: Annotated[Union[bool, None], Field(description='Furnished. Only For Rent')] = None,
                             outdoorSpace: Annotated[Union[bool, None], Field(description='Outdoor space. Only For Rent')] = None,
                             controlledAccess: Annotated[Union[bool, None], Field(description='Controlled access. Only For Rent')] = None,
                             highSpeedInternet: Annotated[Union[bool, None], Field(description='High speed internet. Only For Rent')] = None,
                             elevator: Annotated[Union[bool, None], Field(description='Elevator. Only For Rent')] = None,
                             multiFamilyBuilding: Annotated[Union[bool, None], Field(description='Apartment Community. Only For Rent')] = None,
                             minMonthlyCostPayment: Annotated[Union[int, float, None], Field(description='Min Monthly Cost Payment')] = None,
                             maxMonthlyCostPayment: Annotated[Union[int, float, None], Field(description='Max Monthly Cost Payment')] = None) -> dict: 
    '''Search for properties by parameters. *Note.* If you search by exact address, the endpoint will return only zpid, or list of `zpid`s if it's a building with many units or `lotId`s for building. **To get more information about a property by `zpid`, use a `/property` endpoint. For `lotId` use a `/building` endpoint.** `location` is required if `polygon` and `coordinates` are empty.'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyExtendedSearch'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
        'page': page,
        'status_type': status_type,
        'home_type': home_type,
        'sort': sort,
        'polygon': polygon,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
        'rentMinPrice': rentMinPrice,
        'rentMaxPrice': rentMaxPrice,
        'bathsMin': bathsMin,
        'bathsMax': bathsMax,
        'bedsMin': bedsMin,
        'bedsMax': bedsMax,
        'sqftMin': sqftMin,
        'sqftMax': sqftMax,
        'buildYearMin': buildYearMin,
        'buildYearMax': buildYearMax,
        'daysOn': daysOn,
        'soldInLast': soldInLast,
        'isBasementFinished': isBasementFinished,
        'isBasementUnfinished': isBasementUnfinished,
        'isPendingUnderContract': isPendingUnderContract,
        'isAcceptingBackupOffers': isAcceptingBackupOffers,
        'isComingSoon': isComingSoon,
        'otherListings': otherListings,
        'isNewConstruction': isNewConstruction,
        'keywords': keywords,
        'lotSizeMin': lotSizeMin,
        'lotSizeMax': lotSizeMax,
        'saleByAgent': saleByAgent,
        'saleByOwner': saleByOwner,
        'isForSaleForeclosure': isForSaleForeclosure,
        'isWaterfront': isWaterfront,
        'hasPool': hasPool,
        'hasAirConditioning': hasAirConditioning,
        'isCityView': isCityView,
        'isMountainView': isMountainView,
        'isWaterView': isWaterView,
        'isParkView': isParkView,
        'isOpenHousesOnly': isOpenHousesOnly,
        'is3dHome': is3dHome,
        'coordinates': coordinates,
        'hoa': hoa,
        'includeHomesWithNoHoaData': includeHomesWithNoHoaData,
        'isAuction': isAuction,
        'schools': schools,
        'schoolsRating': schoolsRating,
        'includeUnratedSchools': includeUnratedSchools,
        'hasGarage': hasGarage,
        'parkingSpots': parkingSpots,
        'isForeclosed': isForeclosed,
        'isPreForeclosure': isPreForeclosure,
        'isEntirePlace': isEntirePlace,
        'isRoom': isRoom,
        'largeDogsAllowed': largeDogsAllowed,
        'smallDogsAllowed': smallDogsAllowed,
        'catsAllowed': catsAllowed,
        'noPets': noPets,
        'moveInDate': moveInDate,
        'parkingAvailable': parkingAvailable,
        'inUnitLaundry': inUnitLaundry,
        'acceptsApplications': acceptsApplications,
        'incomeRestricted': incomeRestricted,
        'hardwoodFloor': hardwoodFloor,
        'disabledAccess': disabledAccess,
        'utilitiesIncluded': utilitiesIncluded,
        'shortTermLease': shortTermLease,
        'furnished': furnished,
        'outdoorSpace': outdoorSpace,
        'controlledAccess': controlledAccess,
        'highSpeedInternet': highSpeedInternet,
        'elevator': elevator,
        'multiFamilyBuilding': multiFamilyBuilding,
        'minMonthlyCostPayment': minMonthlyCostPayment,
        'maxMonthlyCostPayment': maxMonthlyCostPayment,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()


async def fetch_detection(session, payload):
    url = 'https://zillow-com1.p.rapidapi.com/propertyExtendedSearch'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com',
               'x-rapidapi-key': rapid_api_key}
    logging.info(payload)
    async with session.get(url, headers=headers, params=payload) as resp:
        res = await resp.json()
    logging.info(len(res.get("props", [])))

    return res


@mcp.tool()
async def property_search_complete_list(location: Annotated[Union[str, None], Field(description='Location details (address, county, neighborhood or Zip code). It is required if the polygon or coordinates is empty. The maximum number of locations (city, zip code) is 5, separate location by ; Multi location /propertyExtendedSearch?location=78013;78014;New York, NY The maximum number of locations is 5 Max length: 100 Please note that for the ZIP Code Type PO Box there will be empty results.')] = None,
                             status_type: Annotated[Literal['ForSale', 'ForRent', 'RecentlySold', None], Field(description='Valid values: ForSale, ForRent, RecentlySold')] = None,
                             home_type: Annotated[Union[str, None], Field(description='Property type comma-separated or empty for all types: For Rent Townhomes Houses Apartments_Condos_Co-ops For others: Multi-family Apartments Houses Manufactured Condos LotsLand Townhomes')] = None,
                             sort: Annotated[Union[str, None], Field(description='For status_type = ForSale OR RecentlySold are available: Homes_for_You Price_High_Low Price_Low_High Newest Bedrooms Bathrooms Square_Feet Lot_Size default Homes_for_You For status_type = ForRent are available: Verified_Source Payment_High_Low Payment_Low_High Newest Bedrooms Bathrooms Square_Feet Lot_Size default Verified_Source')] = None,
                             polygon: Annotated[Union[str, None], Field(description='Format: lon lat,lon1 lat1,lon2 lat2 It is required if the location or coordinates is empty. The last pair must be the same as the first pair.')] = None,
                             minPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForSale OR RecentlySold you can filter by min price. Default: 0')] = None,
                             maxPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForSale OR RecentlySold you can filter by max price. Default: 0')] = None,
                             rentMinPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForRent you can filter by min rent price. Default: 0')] = None,
                             rentMaxPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForRent you can filter by max rent price. Default: 0')] = None,
                             bathsMin: Annotated[Union[int, float, None], Field(description='Bathrooms min count Default: 0')] = None,
                             bathsMax: Annotated[Union[int, float, None], Field(description='Bathrooms max count Default: 0')] = None,
                             bedsMin: Annotated[Union[int, float, None], Field(description='Bedrooms min count Default: 0')] = None,
                             bedsMax: Annotated[Union[int, float, None], Field(description='Bedrooms max count Default: 0')] = None,
                             sqftMin: Annotated[Union[int, float, None], Field(description='Square Feet min value Default: 0')] = None,
                             sqftMax: Annotated[Union[int, float, None], Field(description='Square Feet max value. Default: 0')] = None,
                             buildYearMin: Annotated[Union[int, float, None], Field(description='Year Built min value. Default: 0')] = None,
                             buildYearMax: Annotated[Union[int, float, None], Field(description='Year Built max value. Default: 0')] = None,
                             daysOn: Annotated[Union[str, None], Field(description="Days on Z. Use with status_type='ForSale' or status_type='ForRent' Available values: 1,7,14,30,90,6m,12m,24m,36m")] = None,
                             soldInLast: Annotated[Union[str, None], Field(description="'Sold In Last' on Z. Use with status_type='RecentlySold'. Available values: 1,7,14,30,90,6m,12m,24m,36m")] = None,
                             isBasementFinished: Annotated[Union[int, float, None], Field(description='Basement filter. Set it to 1 if needed. Default: 0')] = None,
                             isBasementUnfinished: Annotated[Union[int, float, None], Field(description='Basement filter. Set it to 1 if needed. Default: 0')] = None,
                             isPendingUnderContract: Annotated[Union[int, float, None], Field(description='Pending & Under Contract filter. Set it to 1 if needed. Default: 0')] = None,
                             isAcceptingBackupOffers: Annotated[Union[int, float, None], Field(description='Accepting Backup Offers filter. Set it to 1 if needed. Default: 0')] = None,
                             isComingSoon: Annotated[Union[bool, None], Field(description='Coming Soon listings are homes that will soon be on the market.. Set it to 1 if needed.')] = None,
                             otherListings: Annotated[Union[bool, None], Field(description='If set to 1, the results will only include data from the Other Listings tab.')] = None,
                             isNewConstruction: Annotated[Union[bool, None], Field(description='New Construction filter. Set it to 1 or true if you only need properties with New Construction status.')] = None,
                             keywords: Annotated[Union[str, None], Field(description='Filter with keywords.')] = None,
                             lotSizeMin: Annotated[Union[str, None], Field(description='Available values: 1,000 sqft 2,000 sqft 3,000 sqft 4,000 sqft 5,000 sqft 7,500 sqft 1/4 acre/10,890 sqft 1/2 acre/21,780 sqft 1 acre/43,560 sqft')] = None,
                             lotSizeMax: Annotated[Union[str, None], Field(description='Available values: 1,000 sqft 2,000 sqft 3,000 sqft 4,000 sqft 5,000 sqft 7,500 sqft 1/4 acre/10,890 sqft 1/2 acre/21,780 sqft 1 acre/43,560 sqft 2 acres/87,120 sqft 5 acres/217,800 sqft 10 acres/435,600 sqft 20 acres/871,200 sqft 50 acres/2,178,000 sqft 100 acres/4,356,000 sqft')] = None,
                             saleByAgent: Annotated[Union[str, None], Field(description='Default - true. To get FSBO set saleByAgent=false&saleByOwner=true&otherListings=true.')] = None,
                             saleByOwner: Annotated[Union[str, None], Field(description='Default - true. To get only FSBO set saleByAgent=false&saleByOwner=true&otherListings=true')] = None,
                             isForSaleForeclosure: Annotated[Union[bool, None], Field(description='If you only need to get ForSaleForeclosure set to true or 1.')] = None,
                             isWaterfront: Annotated[Union[bool, None], Field(description='')] = None,
                             hasPool: Annotated[Union[bool, None], Field(description='')] = None,
                             hasAirConditioning: Annotated[Union[bool, None], Field(description='')] = None,
                             isCityView: Annotated[Union[bool, None], Field(description='')] = None,
                             isMountainView: Annotated[Union[bool, None], Field(description='')] = None,
                             isWaterView: Annotated[Union[bool, None], Field(description='')] = None,
                             isParkView: Annotated[Union[bool, None], Field(description='')] = None,
                             isOpenHousesOnly: Annotated[Union[bool, None], Field(description='Must have open house')] = None,
                             is3dHome: Annotated[Union[bool, None], Field(description='Must have 3D Tour')] = None,
                             coordinates: Annotated[Union[str, None], Field(description='It is required if the location or polygon is empty. Format: lon lat,diameter. Diameter in miles from 1 to 99 -118.51750373840332 34.007063913440916,20')] = None,
                             hoa: Annotated[Union[int, float, None], Field(description='Max HOA. Default: 0')] = None,
                             includeHomesWithNoHoaData: Annotated[Union[bool, None], Field(description='Default - true.')] = None,
                             isAuction: Annotated[Union[bool, None], Field(description='Auctions. Default true.')] = None,
                             schools: Annotated[Union[str, None], Field(description='Available values: elementary, public, private, middle, charter, high For multiple selection, separate with comma: middle,high')] = None,
                             schoolsRating: Annotated[Union[str, None], Field(description='Min school ratings. From 1 to 10')] = None,
                             includeUnratedSchools: Annotated[Union[bool, None], Field(description='Include schools with no rating')] = None,
                             hasGarage: Annotated[Union[bool, None], Field(description='Must have a garage. Default value false')] = None,
                             parkingSpots: Annotated[Union[int, float, None], Field(description='Parking Spots. Max value - 4 Default: 0')] = None,
                             isForeclosed: Annotated[Union[bool, None], Field(description='')] = None,
                             isPreForeclosure: Annotated[Union[bool, None], Field(description='')] = None,
                             isEntirePlace: Annotated[Union[bool, None], Field(description="Default - true. Apply when status_type = 'ForRent'. Set it to false if you need only a room.")] = None,
                             isRoom: Annotated[Union[bool, None], Field(
                                 description="Default - false. Apply when status_type = 'ForRent' Set it true and isEntirePlace to false if you need only a room.")] = None,
                             largeDogsAllowed: Annotated[
                                 Union[bool, None], Field(description='Allows large dogs. Only For Rent')] = None,
                             smallDogsAllowed: Annotated[
                                 Union[bool, None], Field(description='Allows small dogs. Only For Rent')] = None,
                             catsAllowed: Annotated[
                                 Union[bool, None], Field(description='Allows cats. Only For Rent')] = None,
                             noPets: Annotated[Union[bool, None], Field(description='No pets. Only For Rent')] = None,
                             moveInDate: Annotated[
                                 Union[str, datetime, None], Field(description='Move-in Date Only For Rent')] = None,
                             parkingAvailable: Annotated[
                                 Union[bool, None], Field(description='On-site Parking. Only For Rent')] = None,
                             inUnitLaundry: Annotated[
                                 Union[bool, None], Field(description='In-unit Laundry. Only For Rent')] = None,
                             acceptsApplications: Annotated[Union[bool, None], Field(
                                 description='Accepts Zillow Applications. Only For Rent')] = None,
                             incomeRestricted: Annotated[
                                 Union[bool, None], Field(description='Income restricted. Only For Rent')] = None,
                             hardwoodFloor: Annotated[
                                 Union[bool, None], Field(description='Hardwood Floors. Only For Rent')] = None,
                             disabledAccess: Annotated[
                                 Union[bool, None], Field(description='Disabled Access. Only For Rent')] = None,
                             utilitiesIncluded: Annotated[
                                 Union[bool, None], Field(description='Utilities Included. Only For Rent')] = None,
                             shortTermLease: Annotated[Union[bool, None], Field(
                                 description='Short term lease available. Only For Rent')] = None,
                             furnished: Annotated[
                                 Union[bool, None], Field(description='Furnished. Only For Rent')] = None,
                             outdoorSpace: Annotated[
                                 Union[bool, None], Field(description='Outdoor space. Only For Rent')] = None,
                             controlledAccess: Annotated[
                                 Union[bool, None], Field(description='Controlled access. Only For Rent')] = None,
                             highSpeedInternet: Annotated[
                                 Union[bool, None], Field(description='High speed internet. Only For Rent')] = None,
                             elevator: Annotated[
                                 Union[bool, None], Field(description='Elevator. Only For Rent')] = None,
                             multiFamilyBuilding: Annotated[
                                 Union[bool, None], Field(description='Apartment Community. Only For Rent')] = None,
                             minMonthlyCostPayment: Annotated[
                                 Union[int, float, None], Field(description='Min Monthly Cost Payment')] = None,
                             maxMonthlyCostPayment: Annotated[Union[int, float, None], Field(
                                 description='Max Monthly Cost Payment')] = None) -> dict:
    '''Search for complete list of properties by parameters. *Note.* If you search by exact address, the endpoint will return only zpid, or list of `zpid`s if it's a building with many units or `lotId`s for building. **To get more information about a property by `zpid`, use a `/property` endpoint. For `lotId` use a `/building` endpoint.** `location` is required if `polygon` and `coordinates` are empty.'''

    payload = {
        'location': location,
        'status_type': status_type,
        'home_type': home_type,
        'sort': sort,
        'polygon': polygon,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
        'rentMinPrice': rentMinPrice,
        'rentMaxPrice': rentMaxPrice,
        'bathsMin': bathsMin,
        'bathsMax': bathsMax,
        'bedsMin': bedsMin,
        'bedsMax': bedsMax,
        'sqftMin': sqftMin,
        'sqftMax': sqftMax,
        'buildYearMin': buildYearMin,
        'buildYearMax': buildYearMax,
        'daysOn': daysOn,
        'soldInLast': soldInLast,
        'isBasementFinished': isBasementFinished,
        'isBasementUnfinished': isBasementUnfinished,
        'isPendingUnderContract': isPendingUnderContract,
        'isAcceptingBackupOffers': isAcceptingBackupOffers,
        'isComingSoon': isComingSoon,
        'otherListings': otherListings,
        'isNewConstruction': isNewConstruction,
        'keywords': keywords,
        'lotSizeMin': lotSizeMin,
        'lotSizeMax': lotSizeMax,
        'saleByAgent': saleByAgent,
        'saleByOwner': saleByOwner,
        'isForSaleForeclosure': isForSaleForeclosure,
        'isWaterfront': isWaterfront,
        'hasPool': hasPool,
        'hasAirConditioning': hasAirConditioning,
        'isCityView': isCityView,
        'isMountainView': isMountainView,
        'isWaterView': isWaterView,
        'isParkView': isParkView,
        'isOpenHousesOnly': isOpenHousesOnly,
        'is3dHome': is3dHome,
        'coordinates': coordinates,
        'hoa': hoa,
        'includeHomesWithNoHoaData': includeHomesWithNoHoaData,
        'isAuction': isAuction,
        'schools': schools,
        'schoolsRating': schoolsRating,
        'includeUnratedSchools': includeUnratedSchools,
        'hasGarage': hasGarage,
        'parkingSpots': parkingSpots,
        'isForeclosed': isForeclosed,
        'isPreForeclosure': isPreForeclosure,
        'isEntirePlace': isEntirePlace,
        'isRoom': isRoom,
        'largeDogsAllowed': largeDogsAllowed,
        'smallDogsAllowed': smallDogsAllowed,
        'catsAllowed': catsAllowed,
        'noPets': noPets,
        'moveInDate': moveInDate,
        'parkingAvailable': parkingAvailable,
        'inUnitLaundry': inUnitLaundry,
        'acceptsApplications': acceptsApplications,
        'incomeRestricted': incomeRestricted,
        'hardwoodFloor': hardwoodFloor,
        'disabledAccess': disabledAccess,
        'utilitiesIncluded': utilitiesIncluded,
        'shortTermLease': shortTermLease,
        'furnished': furnished,
        'outdoorSpace': outdoorSpace,
        'controlledAccess': controlledAccess,
        'highSpeedInternet': highSpeedInternet,
        'elevator': elevator,
        'multiFamilyBuilding': multiFamilyBuilding,
        'minMonthlyCostPayment': minMonthlyCostPayment,
        'maxMonthlyCostPayment': maxMonthlyCostPayment,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    payloads = []
    for i in range(1, 6):
        page_payload = deepcopy(payload)
        page_payload["page"] = i
        payloads.append(page_payload)
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        fetches = [fetch_detection(session, payload) for payload in payloads]
        fetch_results = await asyncio.gather(*fetches)

    fetch_results = [fr["props"] for fr in fetch_results if fr and "props" in fr]

    result = sum(fetch_results, [])
    return result


@mcp.tool()
def property_by_polygon(polygon: Annotated[str, Field(description='Format: lon lat,lon1 lat1,lon2 lat2 The last pair must be the same as the first pair.')],
                        page: Annotated[Union[int, float, None], Field(description='Page number if at the previous response totalPages > 1. Max value is 20. To be able to access more data, you can break down your request by dividing it into price groups using the minPrice and maxPrice parameters. For example 0 - 100,000, 100,001 - 500,000, 500,001 - 800,000 and so on. This trick will help you to get more data. Default: 0')] = None,
                        status_type: Annotated[Literal['ForSale', 'ForRent', 'RecentlySold', None], Field(description='Valid values: ForSale, ForRent, RecentlySold')] = None,
                        home_type: Annotated[Union[str, None], Field(description='Property type comma-separated or empty for all types: For Rent Townhomes Houses Apartments_Condos_Co-ops For others: Multi-family Apartments Houses Manufactured Condos LotsLand Townhomes')] = None,
                        sort: Annotated[Union[str, None], Field(description='For status_type = ForSale OR RecentlySold are available: Homes_for_You Price_High_Low Price_Low_High Newest Bedrooms Bathrooms Square_Feet Lot_Size default Homes_for_You For status_type = ForRent are available: Verified_Source Payment_High_Low Payment_Low_High Newest Bedrooms Bathrooms Square_Feet Lot_Size default Verified_Source')] = None,
                        minPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForSale OR RecentlySold you can filter by min price. Default: 0')] = None,
                        maxPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForSale OR RecentlySold you can filter by max price. Default: 0')] = None,
                        rentMinPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForRent you can filter by min rent price. Default: 0')] = None,
                        rentMaxPrice: Annotated[Union[int, float, None], Field(description='If status_type = ForRent you can filter by max rent price. Default: 0')] = None,
                        bathsMin: Annotated[Union[int, float, None], Field(description='Bathrooms min count Default: 0')] = None,
                        bathsMax: Annotated[Union[int, float, None], Field(description='Bathrooms max count Default: 0')] = None,
                        bedsMin: Annotated[Union[int, float, None], Field(description='Bedrooms min count Default: 0')] = None,
                        bedsMax: Annotated[Union[int, float, None], Field(description='Bedrooms max count Default: 0')] = None,
                        sqftMin: Annotated[Union[int, float, None], Field(description='Square Feet min value Default: 0')] = None,
                        sqftMax: Annotated[Union[int, float, None], Field(description='Square Feet max value. Default: 0')] = None,
                        buildYearMin: Annotated[Union[int, float, None], Field(description='Year Built min value. Default: 0')] = None,
                        buildYearMax: Annotated[Union[int, float, None], Field(description='Year Built max value. Default: 0')] = None,
                        daysOn: Annotated[Union[str, None], Field(description="Days on Z. Use with status_type='ForSale' or status_type='ForRent' Available values: 1,7,14,30,90,6m,12m,24m,36m")] = None,
                        soldInLast: Annotated[Union[str, None], Field(description="'Sold In Last' on Z. Use with status_type='RecentlySold'. Available values: 1,7,14,30,90,6m,12m,24m,36m")] = None,
                        isBasementFinished: Annotated[Union[int, float, None], Field(description='Basement filter. Set it to 1 if needed. Default: 0')] = None,
                        isBasementUnfinished: Annotated[Union[int, float, None], Field(description='Basement filter. Set it to 1 if needed. Default: 0')] = None,
                        isPendingUnderContract: Annotated[Union[int, float, None], Field(description='Pending & Under Contract filter. Set it to 1 if needed. Default: 0')] = None,
                        isAcceptingBackupOffers: Annotated[Union[int, float, None], Field(description='Accepting Backup Offers filter. Set it to 1 if needed. Default: 0')] = None,
                        isComingSoon: Annotated[Union[bool, None], Field(description='Coming Soon listings are homes that will soon be on the market.. Set it to 1 if needed.')] = None,
                        otherListings: Annotated[Union[int, float, None], Field(description='If set to 1, the results will only include data from the Other Listings tab. Default: 0')] = None,
                        isNewConstruction: Annotated[Union[bool, None], Field(description='New Construction filter. Set it to 1 if you only need properties with New Construction status.')] = None,
                        keywords: Annotated[Union[str, None], Field(description='Filter with keywords.')] = None,
                        lotSizeMin: Annotated[Union[str, None], Field(description='Available values: 1,000 sqft 2,000 sqft 3,000 sqft 4,000 sqft 5,000 sqft 7,500 sqft 1/4 acre/10,890 sqft 1/2 acre/21,780 sqft 1 acre/43,560 sqft')] = None,
                        lotSizeMax: Annotated[Union[str, None], Field(description='Available values: 1,000 sqft 2,000 sqft 3,000 sqft 4,000 sqft 5,000 sqft 7,500 sqft 1/4 acre/10,890 sqft 1/2 acre/21,780 sqft 1 acre/43,560 sqft 2 acres/87,120 sqft 5 acres/217,800 sqft 10 acres/435,600 sqft 20 acres/871,200 sqft 50 acres/2,178,000 sqft 100 acres/4,356,000 sqft')] = None,
                        saleByAgent: Annotated[Union[str, None], Field(description='Default - true. If you only need to get FSBO set to false or 0.')] = None,
                        saleByOwner: Annotated[Union[str, None], Field(description='Default - true. If you only need to get FSBA set to false or 0.')] = None,
                        isForSaleForeclosure: Annotated[Union[bool, None], Field(description='If you only need to get ForSaleForeclosure set to true or 1.')] = None,
                        isWaterfront: Annotated[Union[bool, None], Field(description='')] = None,
                        hasPool: Annotated[Union[bool, None], Field(description='')] = None,
                        hasAirConditioning: Annotated[Union[bool, None], Field(description='')] = None,
                        isCityView: Annotated[Union[bool, None], Field(description='')] = None,
                        isMountainView: Annotated[Union[bool, None], Field(description='')] = None,
                        isWaterView: Annotated[Union[bool, None], Field(description='')] = None,
                        isParkView: Annotated[Union[bool, None], Field(description='')] = None,
                        isOpenHousesOnly: Annotated[Union[bool, None], Field(description='Must have open house')] = None,
                        is3dHome: Annotated[Union[bool, None], Field(description='Must have 3D Tour')] = None,
                        hoa: Annotated[Union[int, float, None], Field(description='Max HOA. Default: 0')] = None,
                        includeHomesWithNoHoaData: Annotated[Union[bool, None], Field(description='Default - true.')] = None,
                        isAuction: Annotated[Union[bool, None], Field(description='Auctions. Default true.')] = None,
                        schools: Annotated[Union[str, None], Field(description='Available values: elementary, public, private, middle, charter, high For multiple selection, separate with comma: middle,high')] = None,
                        schoolsRating: Annotated[Union[str, None], Field(description='Min school ratings. From 1 to 10')] = None,
                        includeUnratedSchools: Annotated[Union[bool, None], Field(description='Include schools with no rating')] = None,
                        hasGarage: Annotated[Union[bool, None], Field(description='Must have a garage. Default value false')] = None,
                        parkingSpots: Annotated[Union[int, float, None], Field(description='Parking Spots. Max value - 4 Default: 0')] = None,
                        isForeclosed: Annotated[Union[bool, None], Field(description='')] = None,
                        isEntirePlace: Annotated[Union[bool, None], Field(description="Default - true. Apply when status_type = 'ForRent'. Set it to false if you need only a room.")] = None,
                        isPreForeclosure: Annotated[Union[bool, None], Field(description='')] = None,
                        isRoom: Annotated[Union[bool, None], Field(description="Default - false. Apply when status_type = 'ForRent' Set it true and isEntirePlace to false if you need only a room.")] = None,
                        largeDogsAllowed: Annotated[Union[bool, None], Field(description='Allows large dogs. Only For Rent')] = None,
                        smallDogsAllowed: Annotated[Union[bool, None], Field(description='Allows large dogs. Only For Rent')] = None,
                        catsAllowed: Annotated[Union[bool, None], Field(description='Allows cats. Only For Rent')] = None,
                        noPets: Annotated[Union[bool, None], Field(description='Allows cats. Only For Rent')] = None,
                        moveInDate: Annotated[Union[str, datetime, None], Field(description='Move-in Date Only For Rent')] = None,
                        parkingAvailable: Annotated[Union[bool, None], Field(description='On-site Parking. Only For Rent')] = None,
                        inUnitLaundry: Annotated[Union[bool, None], Field(description='In-unit Laundry. Only For Rent')] = None,
                        acceptsApplications: Annotated[Union[bool, None], Field(description='Accepts Zillow Applications. Only For Rent')] = None,
                        incomeRestricted: Annotated[Union[bool, None], Field(description='Income restricted. Only For Rent')] = None,
                        hardwoodFloor: Annotated[Union[bool, None], Field(description='Hardwood Floors. Only For Rent')] = None,
                        disabledAccess: Annotated[Union[bool, None], Field(description='Disabled Access. Only For Rent')] = None,
                        utilitiesIncluded: Annotated[Union[bool, None], Field(description='Utilities Included. Only For Rent')] = None,
                        shortTermLease: Annotated[Union[bool, None], Field(description='Short term lease available. Only For Rent')] = None,
                        furnished: Annotated[Union[bool, None], Field(description='Furnished. Only For Rent')] = None,
                        outdoorSpace: Annotated[Union[bool, None], Field(description='Outdoor space. Only For Rent')] = None,
                        controlledAccess: Annotated[Union[bool, None], Field(description='Controlled access. Only For Rent')] = None,
                        highSpeedInternet: Annotated[Union[bool, None], Field(description='High speed internet. Only For Rent')] = None,
                        elevator: Annotated[Union[bool, None], Field(description='Elevator. Only For Rent')] = None,
                        multiFamilyBuilding: Annotated[Union[bool, None], Field(description='Apartment Community. Only For Rent')] = None,
                        minMonthlyCostPayment: Annotated[Union[int, float, None], Field(description='Min Monthly Cost Payment Default: 0')] = None,
                        maxMonthlyCostPayment: Annotated[Union[int, float, None], Field(description='Max Monthly Cost Payment Default: 0')] = None) -> dict: 
    '''Search for properties using polygon of points.'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyByPolygon'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'polygon': polygon,
        'page': page,
        'status_type': status_type,
        'home_type': home_type,
        'sort': sort,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
        'rentMinPrice': rentMinPrice,
        'rentMaxPrice': rentMaxPrice,
        'bathsMin': bathsMin,
        'bathsMax': bathsMax,
        'bedsMin': bedsMin,
        'bedsMax': bedsMax,
        'sqftMin': sqftMin,
        'sqftMax': sqftMax,
        'buildYearMin': buildYearMin,
        'buildYearMax': buildYearMax,
        'daysOn': daysOn,
        'soldInLast': soldInLast,
        'isBasementFinished': isBasementFinished,
        'isBasementUnfinished': isBasementUnfinished,
        'isPendingUnderContract': isPendingUnderContract,
        'isAcceptingBackupOffers': isAcceptingBackupOffers,
        'isComingSoon': isComingSoon,
        'otherListings': otherListings,
        'isNewConstruction': isNewConstruction,
        'keywords': keywords,
        'lotSizeMin': lotSizeMin,
        'lotSizeMax': lotSizeMax,
        'saleByAgent': saleByAgent,
        'saleByOwner': saleByOwner,
        'isForSaleForeclosure': isForSaleForeclosure,
        'isWaterfront': isWaterfront,
        'hasPool': hasPool,
        'hasAirConditioning': hasAirConditioning,
        'isCityView': isCityView,
        'isMountainView': isMountainView,
        'isWaterView': isWaterView,
        'isParkView': isParkView,
        'isOpenHousesOnly': isOpenHousesOnly,
        'is3dHome': is3dHome,
        'hoa': hoa,
        'includeHomesWithNoHoaData': includeHomesWithNoHoaData,
        'isAuction': isAuction,
        'schools': schools,
        'schoolsRating': schoolsRating,
        'includeUnratedSchools': includeUnratedSchools,
        'hasGarage': hasGarage,
        'parkingSpots': parkingSpots,
        'isForeclosed': isForeclosed,
        'isEntirePlace': isEntirePlace,
        'isPreForeclosure': isPreForeclosure,
        'isRoom': isRoom,
        'largeDogsAllowed': largeDogsAllowed,
        'smallDogsAllowed': smallDogsAllowed,
        'catsAllowed': catsAllowed,
        'noPets': noPets,
        'moveInDate': moveInDate,
        'parkingAvailable': parkingAvailable,
        'inUnitLaundry': inUnitLaundry,
        'acceptsApplications': acceptsApplications,
        'incomeRestricted': incomeRestricted,
        'hardwoodFloor': hardwoodFloor,
        'disabledAccess': disabledAccess,
        'utilitiesIncluded': utilitiesIncluded,
        'shortTermLease': shortTermLease,
        'furnished': furnished,
        'outdoorSpace': outdoorSpace,
        'controlledAccess': controlledAccess,
        'highSpeedInternet': highSpeedInternet,
        'elevator': elevator,
        'multiFamilyBuilding': multiFamilyBuilding,
        'minMonthlyCostPayment': minMonthlyCostPayment,
        'maxMonthlyCostPayment': maxMonthlyCostPayment,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def rent_estimate(propertyType: Annotated[Literal['SingleFamily', 'Condo', 'MultiFamily', 'Townhouse', 'Apartment'], Field(description='Valid values: SingleFamily, Condo, MultiFamily, Townhouse, Apartment')],
                  address: Annotated[Union[str, None], Field(description='')] = None,
                  long: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  lat: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  d: Annotated[Union[int, float, None], Field(description='Diameter in miles. The max and value is 0.5, and the low value is 0.05. The default value is 0.5 Default: 0.5')] = None,
                  beds: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  baths: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  sqftMin: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  sqftMax: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  includeComps: Annotated[Union[bool, None], Field(description='')] = None) -> dict: 
    '''*`address` or `long` and `lat` is required!* For more accuracy use `beds` and `baths` parameters. Will return rent estimates and comparable rentals if need.'''
    url = 'https://zillow-com1.p.rapidapi.com/rentEstimate'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'propertyType': propertyType,
        'address': address,
        'long': long,
        'lat': lat,
        'd': d,
        'beds': beds,
        'baths': baths,
        'sqftMin': sqftMin,
        'sqftMax': sqftMax,
        'includeComps': includeComps,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def location_suggestions(q: Annotated[str, Field(description='State, county, neighborhood, city, street name')]) -> dict: 
    '''Search for a location by name.'''
    url = 'https://zillow-com1.p.rapidapi.com/locationSuggestions'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'q': q,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def property_by_coordinates(long: Annotated[Union[int, float], Field(description='Longitude Default: -118.504744')],
                            lat: Annotated[Union[int, float], Field(description='Latitude Default: 34.01822')],
                            d: Annotated[Union[int, float, None], Field(description='Diameter in miles. The max value is 0.5, and the low value is 0.05. The default value is 0.1 Default: 0.1')] = None,
                            includeSold: Annotated[Union[bool, None], Field(description='Include to results sold properties. true or 1 to include (default). false or 0 to exclude.')] = None) -> dict: 
    '''Search the property by coordinates. *Note.* The endpoint will return only an array of zpid. To get more information use `/property` endpoint. If you need additional filters, you can use `/propertyExtendedSearch` with a parameter `coordinates` or `polygon`.'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyByCoordinates'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'long': long,
        'lat': lat,
        'd': d,
        'includeSold': includeSold,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def search_by_url(url: Annotated[str, Field(description='This URL you can get from browser address bar after you apply all parameters on Zillow site.')],
                  page: Annotated[Union[int, float, None], Field(description='Default: 0')] = None) -> dict: 
    '''Get a list of properties by providing Zillow's search results URL'''
    url = 'https://zillow-com1.p.rapidapi.com/searchByUrl'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'url': url,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def property_by_mls(mls: Annotated[str, Field(description='MLS #')]) -> dict: 
    '''Search for the property by MLS #. *Note.* The endpoint will return an array of `zpid`. To get more information, use `/property` endpoint. If we find more than one address with the given MLS, we will send them in `otherAddress` key. You can check them for additional.'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyByMls'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'mls': mls,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def images(zpid: Annotated[Union[int, float], Field(description='Default: 2080998890')],
           property_url: Annotated[Union[str, None], Field(description='Full page URL - https://www.zillow.com/homedetails/101-California-Ave-UNIT-506-Santa-Monica-CA-90403/20485717_zpid/')] = None) -> dict: 
    '''Property images and videos.'''
    url = 'https://zillow-com1.p.rapidapi.com/images'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def price_and_tax_history(zpid: Annotated[Union[str, None], Field(description='')] = None,
                          property_url: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''History of Property Taxes and Prices. `zpid` or `property_url` is required.'''
    url = 'https://zillow-com1.p.rapidapi.com/priceAndTaxHistory'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def property_comps(zpid: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                   property_url: Annotated[Union[str, None], Field(description='')] = None,
                   address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Get property comps by `zpid` or `property_url` or `address`.'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyComps'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def walk_and_transit_score(zpid: Annotated[str, Field(description='Unique ID that Zillow gives to each property.')]) -> dict: 
    '''Data about walk, bike and transit scores by zpid.'''
    url = 'https://zillow-com1.p.rapidapi.com/walkAndTransitScore'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def building(lotId: Annotated[Union[int, float, None], Field(description='lotId = buildingId (you can get it a response from the /property endpoint). Only one of the three parameters is required. Default: 1001411303')] = None,
             buildingId: Annotated[Union[str, None], Field(description='You can get it a response from the /property endpoint. Only one of the three parameters is required.')] = None,
             url: Annotated[Union[str, None], Field(description='Building URL https://www.zillow.com/b/48-east-ave-austin-tx-9LRMhF/ or /apartments/portland-or/charmain-apartments/9VLnvH/ Only one of the three parameters is required.')] = None) -> dict: 
    '''Building details. *Only for rent apartments.* Only one of the three parameters is required.'''
    url = 'https://zillow-com1.p.rapidapi.com/building'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'lotId': lotId,
        'buildingId': buildingId,
        'url': url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def zestimate(zpid: Annotated[Union[str, None], Field(description='The zpid or address or property_url parameter is required.')] = None,
              address: Annotated[Union[str, None], Field(description='The zpid or address or property_url parameter is required.')] = None,
              property_url: Annotated[Union[str, None], Field(description='The zpid or address or property_url parameter is required.')] = None) -> dict: 
    '''Get Zestimate value by `zpid` or `address` or `URL`.'''
    url = 'https://zillow-com1.p.rapidapi.com/zestimate'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'address': address,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def zestimate_history(zpid: Annotated[Union[int, float, None], Field(description='Unique ID that Zillow gives to each property. Default: 13172523')] = None,
                      property_url: Annotated[Union[str, None], Field(description='Property page full URL - https://www.zillow.com/homedetails/7646-S-Cook-Way-Centennial-CO-80122/13172523_zpid/')] = None,
                      address: Annotated[Union[str, None], Field(description='The zpid or address or property_url parameter is required.')] = None) -> dict: 
    '''Zestimate History for property by `zpid` or `url`. Result has format where t - time, v - zestimate value.'''
    url = 'https://zillow-com1.p.rapidapi.com/zestimateHistory'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def ping() -> dict: 
    '''Ping'''
    url = 'https://zillow-com1.p.rapidapi.com/ping'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def build_web_url(location: Annotated[Union[str, None], Field(description='You can pass: state, city, zipcode or county.')] = None,
                  home_type: Annotated[Union[str, None], Field(description='Property type comma-separated or empty for all types: Multi-family Apartments Houses Manufactured Condos LotsLand Townhomes')] = None,
                  beds: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  baths: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  sqft: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  isAuction: Annotated[Union[bool, None], Field(description='')] = None,
                  min_price: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                  max_price: Annotated[Union[int, float, None], Field(description='Default: 0')] = None) -> dict: 
    '''**Beta** Build Web Url.'''
    url = 'https://zillow-com1.p.rapidapi.com/buildWebUrl'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
        'home_type': home_type,
        'beds': beds,
        'baths': baths,
        'sqft': sqft,
        'isAuction': isAuction,
        'min_price': min_price,
        'max_price': max_price,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_history_local_rental_rates(zpid: Annotated[Union[str, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                                     property_url: Annotated[Union[str, None], Field(description='Property page full URL')] = None,
                                     address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Rent Zestimate History'''
    url = 'https://zillow-com1.p.rapidapi.com/valueHistory/localRentalRates'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_history_zestimate_percent_change(zpid: Annotated[Union[str, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                                           property_url: Annotated[Union[str, None], Field(description='Property page full URL')] = None,
                                           address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Zestimate Percent Change'''
    url = 'https://zillow-com1.p.rapidapi.com/valueHistory/zestimatePercentChange'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_history_local_home_values(zpid: Annotated[Union[str, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                                    property_url: Annotated[Union[str, None], Field(description='Property page full URL')] = None,
                                    address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Zestimate Value History'''
    url = 'https://zillow-com1.p.rapidapi.com/valueHistory/localHomeValues'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_history_listing_prices(zpid: Annotated[Union[str, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                                 property_url: Annotated[Union[str, None], Field(description='Property page full URL.')] = None,
                                 address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Local Listing Prices'''
    url = 'https://zillow-com1.p.rapidapi.com/valueHistory/listingPrices'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_history_tax_assessment(zpid: Annotated[Union[str, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                                 property_url: Annotated[Union[str, None], Field(description='Property page full URL')] = None,
                                 address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Tax Assessment History'''
    url = 'https://zillow-com1.p.rapidapi.com/valueHistory/taxAssessment'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_history_tax_paid(zpid: Annotated[Union[str, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                           property_url: Annotated[Union[str, None], Field(description='Property page full URL')] = None,
                           address: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Tax Paid History'''
    url = 'https://zillow-com1.p.rapidapi.com/valueHistory/taxPaid'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
        'address': address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def value_estimate(propertyType: Annotated[Literal['SingleFamily', 'Condo', 'MultiFamily', 'Townhouse', 'Apartment'], Field(description='Valid values: SingleFamily, Condo, MultiFamily, Townhouse, Apartment')],
                   address: Annotated[Union[str, None], Field(description='')] = None,
                   long: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                   lat: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                   d: Annotated[Union[int, float, None], Field(description='Diameter in miles. The max and value is 1.5, and the low value is 0.05. The default value is 0.5 Default: 0.5')] = None,
                   beds: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                   baths: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                   sqftMin: Annotated[Union[str, None], Field(description='')] = None,
                   sqftMax: Annotated[Union[str, None], Field(description='')] = None,
                   includeComps: Annotated[Union[bool, None], Field(description='')] = None) -> dict: 
    '''*`address` or `long` and `lat` is required!* For more accuracy use `beds` and `baths` parameters. Will return value estimates and comparable rentals if need.'''
    url = 'https://zillow-com1.p.rapidapi.com/valueEstimate'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'propertyType': propertyType,
        'address': address,
        'long': long,
        'lat': lat,
        'd': d,
        'beds': beds,
        'baths': baths,
        'sqftMin': sqftMin,
        'sqftMax': sqftMax,
        'includeComps': includeComps,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def map_boundary(zip: Annotated[str, Field(description='US zip code')]) -> dict: 
    '''Get map boundary by ZIP code'''
    url = 'https://zillow-com1.p.rapidapi.com/mapBoundary'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zip': zip,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def property_floor_plan(zpid: Annotated[Union[int, float, None], Field(description='Note, not all properties have this information Only those that have a value of true in the isShowcaseListing field, this value can be found by using /property (Property details) endpoint Default: 0')] = None,
                        property_url: Annotated[Union[str, None], Field(description='Full page URL - https://www.zillow.com/homedetails/6361-Blucher-Ave-Van-Nuys-CA-91411/19971282_zpid/')] = None) -> dict: 
    '''Get floorplan images'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyFloorPlan'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def off_market_data(zip: Annotated[str, Field(description='ZIP code. There is no other filter, only by ZIP code. Results include both off-market and on-market data. The data is not very accurate on the border of 2 zip, but if you try the next pages it will work.')],
                    page: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''You can get off-market properties. Results include both off-market and on-market data. Filter only by ZIP code. The data is not very accurate on the border of 2 zip, but if you try the next pages it will work.'''
    url = 'https://zillow-com1.p.rapidapi.com/offMarket'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zip': zip,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def agent_details(username: Annotated[str, Field(description='')]) -> dict: 
    '''Get agent details by username (contact details, active listings, reviews, etc).'''
    url = 'https://zillow-com1.p.rapidapi.com/agentDetails'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'username': username,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def agent_reviews(zuid: Annotated[str, Field(description='Agent unique id - zuid')],
                  page: Annotated[Union[int, float, None], Field(description='Max value: 20. Page size is 5 (max). Default: 1')] = None) -> dict: 
    '''Agent reviews'''
    url = 'https://zillow-com1.p.rapidapi.com/agentReviews'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zuid': zuid,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def agent_active_listings(zuid: Annotated[str, Field(description='Agent unique id - zuid')],
                          page: Annotated[Union[int, float, None], Field(description='Max value: 20 Default: 1')] = None,
                          size: Annotated[Union[int, float, None], Field(description='Max value: 5 Default: 5')] = None) -> dict: 
    '''Agent's active listings. The endpoint will return a list of the property. To get a property details use `/property (Zillow property details)` endpoint.'''
    url = 'https://zillow-com1.p.rapidapi.com/agentActiveListings'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zuid': zuid,
        'page': page,
        'size': size,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def agent_sold_listings(zuid: Annotated[str, Field(description='Agent unique id - zuid')],
                        page: Annotated[Union[int, float, None], Field(description='Max value: 20 Default: 1')] = None,
                        size: Annotated[Union[int, float, None], Field(description='Max value: 5 Default: 5')] = None) -> dict: 
    '''Listings of sold property by agent (`zuid`)'''
    url = 'https://zillow-com1.p.rapidapi.com/agentSoldListings'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zuid': zuid,
        'page': page,
        'size': size,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def agent_rental_listings(zuid: Annotated[str, Field(description='Agent unique id - zuid')],
                          page: Annotated[Union[int, float, None], Field(description='Max value: 20 Default: 1')] = None,
                          size: Annotated[Union[int, float, None], Field(description='Max value: 5 Default: 5')] = None) -> dict: 
    '''Listings of rental property by agent (`zuid`)'''
    url = 'https://zillow-com1.p.rapidapi.com/agentRentalListings'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zuid': zuid,
        'page': page,
        'size': size,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def find_agent_v2(location: Annotated[Union[str, None], Field(description='e.g. Newport Beach or zip code 90278')] = None,
                  name: Annotated[Union[str, None], Field(description='Search by name e.g. Regina Vannicola')] = None,
                  page: Annotated[Union[int, float, None], Field(description='Max value 25')] = None) -> dict: 
    '''Find agent by `name` or `location`'''
    url = 'https://zillow-com1.p.rapidapi.com/findAgentV2'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
        'name': name,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def find_agent(locationText: Annotated[Union[str, None], Field(description='e.g. Newport Beach or zip code 90278')] = None,
               name: Annotated[Union[str, None], Field(description='Search by name e.g. Regina Vannicola')] = None,
               lat: Annotated[Union[str, None], Field(description='e.g. 34.010116')] = None,
               lng: Annotated[Union[str, None], Field(description='e.g. -118.498786')] = None,
               page: Annotated[Union[int, float, None], Field(description='Default: 1')] = None) -> dict: 
    '''**Deprecated!** Find agent by `name` or `location name` or `lat` and `lng`'''
    url = 'https://zillow-com1.p.rapidapi.com/findAgent'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'locationText': locationText,
        'name': name,
        'lat': lat,
        'lng': lng,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def resolve_address_to_zpid(data: Annotated[dict, Field(description='')] = None) -> dict: 
    '''Resolving the addresses from the given file to `zpid`. The limit for the BASIC plan is 10 lines and for the other plans it is 100 lines. ***Cost: 1 request per line!*** Expand ==> Code snippet (Python) [gist.github.com](https://gist.github.com/apimaker001/6ec89060307f8b5d15c0b245e378fbd4) ***How does this work?*** You send a file with the addresses (one per line) and as the answer will receive data, where you will find `jobNumber` field. After some time (2 sec per line) use your `jobNumber` value and `/getJobResults` endpoint to get the results. ***Results example*** **You send the file with lines** 5500 Grand Lake Drive, San Antonio, TX 1636 Sonnet Drive, Grapevine, Texas 76051 2310 fairhill dr newport beach ca 92660 **You will receive the file with lines (format csv: address,zpid)** "5500 Grand Lake Drive, San Antonio, TX",26187246 "1636 Sonnet Drive, Grapevine, Texas 76051",28959146 "2310 fairhill dr newport beach ca 92660",2069242807,25214848'''
    url = 'https://zillow-com1.p.rapidapi.com/resolveAddressToZpid'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@mcp.tool()
def get_job_results(jobNumber: Annotated[Union[int, float], Field(description='Default: 0')]) -> dict: 
    '''Get the result data by `jobNumber`.'''
    url = 'https://zillow-com1.p.rapidapi.com/getJobResults'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'jobNumber': jobNumber,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def remove_job(id: Annotated[Union[int, float], Field(description='Job id Default: 0')]) -> dict: 
    '''Use for remove job from queue by id.'''
    url = 'https://zillow-com1.p.rapidapi.com/removeJob'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'id': id,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def similar_property(zpid: Annotated[Union[int, float, None], Field(description='You can get it from /propertyExtendedSearch or /propertyByCoordinates endpoints, or extract it from a full URL. Default: 2080998890')] = None,
                     property_url: Annotated[Union[str, None], Field(description='Full page URL - https://www.zillow.com/homedetails/101-California-Ave-UNIT-506-Santa-Monica-CA-90403/20485717_zpid/')] = None) -> dict: 
    '''Get similar properties for sale. `zpid` or `property_url` is required parameter.'''
    url = 'https://zillow-com1.p.rapidapi.com/similarProperty'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def similar_sales(zpid: Annotated[Union[int, float, None], Field(description='You can get it from /propertyExtendedSearch or /propertyByCoordinates endpoints, or extract it from a full URL. Default: 19959099')] = None,
                  property_url: Annotated[Union[str, None], Field(description='Full page URL - https://www.zillow.com/homedetails/7301-Lennox-Ave-UNIT-D06-Los-Angeles-CA-91405/19959099_zpid/')] = None) -> dict: 
    '''Recently sold homes with similar features to those passed by zpid home, such as bedrooms, bathrooms, location and square footage. `zpid` or `property_url` is required parameter.'''
    url = 'https://zillow-com1.p.rapidapi.com/similarSales'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def similar_for_rent(zpid: Annotated[Union[int, float, None], Field(description='You can get it from /propertyExtendedSearch or /propertyByCoordinates endpoints, or extract it from a full URL. Default: 246283880')] = None,
                     property_url: Annotated[Union[str, None], Field(description='Full page URL - https://www.zillow.com/homedetails/102-Griffith-Ave-Prattville-AL-36066/77224_zpid/')] = None) -> dict: 
    '''Get similar properties for rent. `zpid` or `property_url` is required parameter.'''
    url = 'https://zillow-com1.p.rapidapi.com/similarForRent'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def market_data(resourceId: Annotated[str, Field(description='Get it from the endpoint /marketLocation response.')],
                beds: Annotated[Literal['0', '1', '2', '3', '4plus', None], Field(description='0 - Studio 1 - 1 bedroom 2 - 2 bedroom 3 - 3 bedroom 4plus - 4 bedroom +')] = None,
                propertyTypes: Annotated[Literal['house', 'apartment_condo', 'townhouse', None], Field(description='Valid values: house, apartment_condo, townhouse')] = None) -> dict: 
    '''**beta version** Rental market summary and year trends. Use zip code as `resourceId` or get `resourceId` for your city in response data from `/marketLocation`.'''
    url = 'https://zillow-com1.p.rapidapi.com/marketData'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'resourceId': resourceId,
        'beds': beds,
        'propertyTypes': propertyTypes,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def market_location(location: Annotated[str, Field(description='Search by city or ZIP')]) -> dict: 
    '''**beta version** Get `resourceId` for city you want.'''
    url = 'https://zillow-com1.p.rapidapi.com/marketLocation'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def other_professionals_search(location: Annotated[str, Field(description='Neighborhood /City /Zip')],
                               type: Annotated[Literal['property_managers', 'inspectors', 'photographers', 'other'], Field(description='Valid values: property_managers, inspectors, photographers, other')],
                               name: Annotated[Union[str, None], Field(description='')] = None,
                               page: Annotated[Union[int, float, None], Field(description='Default: 0')] = None) -> dict: 
    '''Search for other professionals. Check the `type` parameter.'''
    url = 'https://zillow-com1.p.rapidapi.com/otherProfessionals/search'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
        'type': type,
        'name': name,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def other_professionals_reviews(zuid: Annotated[str, Field(description='zuid from search response.')],
                                page: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                                size: Annotated[Union[int, float, None], Field(description='Max value - 20 Default: 0')] = None) -> dict: 
    '''Get reviews'''
    url = 'https://zillow-com1.p.rapidapi.com/otherProfessionals/reviews'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zuid': zuid,
        'page': page,
        'size': size,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def lender_details(screenName: Annotated[str, Field(description='')]) -> dict: 
    '''Get lender details'''
    url = 'https://zillow-com1.p.rapidapi.com/lender/details'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'screenName': screenName,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def lender_reviews(lenderId: Annotated[str, Field(description='')],
                   page: Annotated[Union[int, float, None], Field(description='Default: 0')] = None) -> dict: 
    '''Reviews'''
    url = 'https://zillow-com1.p.rapidapi.com/lender/reviews'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'lenderId': lenderId,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def lender_search(location: Annotated[str, Field(description='City, State or Zip. Only lenders licensed in the state will be displayed.')],
                  lenderName: Annotated[Union[str, None], Field(description='')] = None,
                  page: Annotated[Union[int, float, None], Field(description='Default: 0')] = None) -> dict: 
    '''Search for lender'''
    url = 'https://zillow-com1.p.rapidapi.com/lender/search'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
        'lenderName': lenderName,
        'page': page,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def skip_trace_address_from_file(data: Annotated[dict, Field(description='')] = None) -> dict: 
    '''Resolve Address from File. Check tab `Body` to pickup a **CSV** file. The limit for the BASIC plan is 10 lines and for the other plans it is 100 lines. ***Cost: 5 request per line!***'''
    url = 'https://zillow-com1.p.rapidapi.com/people/addressTrace'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@mcp.tool()
def get_the_result_data_by_jobnumber(jobNumber: Annotated[Union[int, float, None], Field(description='Default: 0')] = None) -> dict: 
    '''Get the result data by jobNumber'''
    url = 'https://zillow-com1.p.rapidapi.com/getJobResults'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'jobNumber': jobNumber,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def people_profile_details(id: Annotated[str, Field(description='ID from /people/searchByAddress endpoint.')]) -> dict: 
    '''Profile Details'''
    url = 'https://zillow-com1.p.rapidapi.com/people/profileDetails'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'id': id,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def people_search_by_address(address: Annotated[str, Field(description='Enter street address to search, example 2246 Tennessee St.')],
                             location: Annotated[str, Field(description='Enter city, state or zip to search')],
                             format: Annotated[Literal['full', 'simple', None], Field(description='simple - will return requested data as a line address,location,phone1,phone2,...,phoneX')] = None) -> dict: 
    '''**deprecated** **beta version** **1 success request will reduce 5 requests from your limit.** We check address, if we can extract data (all names and phones, 2 or 10 does not matter) we subtract 5 from your plan limit. if not, then we subtract 1 from your plan limit Search People By Address'''
    url = 'https://zillow-com1.p.rapidapi.com/people/searchByAddress'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'address': address,
        'location': location,
        'format': format,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def mortgage_rates(program: Annotated[str, Field(description='The loan program. You can select from 1 to 4 programs, separated by commas. Available: Fixed30Year, Fixed20Year, Fixed15Year, Fixed10Year, ARM3, ARM5, ARM7, HomeEquity30Year, HomeEquity30YearDueIn15, HomeEquity15Year, HELOC20Year, HELOC15Year, HELOC10Year')],
                   state: Annotated[Union[str, None], Field(description='The state abbreviation. AK,AL,AR,AS,AZ,CA,CO,CT,DC,DE,FL,GA, GU,HI,IA,ID,IL,IN,KS,KY,LA,MA,MD,ME,MH, MI,MN,MO,MP,MS,MT,NC,ND,NE, NH,NJ,NM,NV,NY,OH,OK,OR,PA,PR,RI,SC,SD,TN,TX,UT,VA,VI,VT,WA,WI,WV,WY,US')] = None,
                   refinance: Annotated[Union[bool, None], Field(description='')] = None,
                   loanType: Annotated[Literal['Conventional', 'FHA', 'VA', 'USDA', 'Other', 'Jumbo', None], Field(description='Valid values: Conventional, FHA, VA, USDA, other, Jumbo')] = None,
                   loanAmount: Annotated[Literal['Conforming', 'SmallConforming', 'SuperConforming', 'Jumbo', 'Micro', None], Field(description='Micro < $100,000 SmallConforming $100,000 - $200,000 Conforming > $200,000 SuperConforming Jumbo')] = None,
                   loanToValue: Annotated[Literal['Normal', 'High', 'VeryHigh', None], Field(description='Normal < 80% High > 80% < 95% VeryHigh >= 95%')] = None,
                   creditScore: Annotated[Literal['Low', 'High', 'VeryHigh', None], Field(description='Low < 680 credit score. High > 680 < 740 VeryHigh > 740')] = None,
                   duration: Annotated[Union[int, float, None], Field(description='From 0 to 4000 Default: 30')] = None) -> dict: 
    '''Get Mortgage Rates by state'''
    url = 'https://zillow-com1.p.rapidapi.com/mortgageRates'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'program': program,
        'state': state,
        'refinance': refinance,
        'loanType': loanType,
        'loanAmount': loanAmount,
        'loanToValue': loanToValue,
        'creditScore': creditScore,
        'duration': duration,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def property_estimate_mortgage(zpid: Annotated[Union[int, float, None], Field(description='Unique ID that Zillow gives to each property.')] = None,
                               property_url: Annotated[Union[str, None], Field(description='')] = None) -> dict: 
    '''Get estimated monthly mortgage payment'''
    url = 'https://zillow-com1.p.rapidapi.com/propertyEstimateMortgage'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zpid': zpid,
        'property_url': property_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def monthly_inventory(zip: Annotated[Union[int, float, None], Field(description='Required if yyyymm is empty. ex. 17249 Default: 0')] = None,
                      yyyymm: Annotated[Union[int, float, None], Field(description='Required if zip is empty. From 201607 to the previous month. Default: 202411')] = None,
                      page: Annotated[Union[int, float, None], Field(description='Default: 0')] = None,
                      limit: Annotated[Union[int, float, None], Field(description='Max 100 per page Default: 10')] = None) -> dict: 
    '''Monthly Inventory. - Active Listing Count, Active Listing Count M/M - Avg Listing Price, Avg Listing Price M/M - Days on Market, Days on Market M/M - New Listing Count, New Listing Count M/M - Median Listing Price, Median Listing Price M/M - Total Listing Count, Total Listing Count M/M - Price Increase Count, Price Increase Count m/M'''
    url = 'https://zillow-com1.p.rapidapi.com/residentialData/monthlyInventory'
    headers = {'x-rapidapi-host': 'zillow-com1.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'zip': zip,
        'yyyymm': yyyymm,
        'page': page,
        'limit': limit,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()



if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
