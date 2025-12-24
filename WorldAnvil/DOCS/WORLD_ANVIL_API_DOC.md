WORLD ANVIL API DOCUMENTATION
V.0.3 (ARAGORN)
Home
 Last updated: June 16th, 2020
Changelog | Upcoming Updates
Welcome
Welcome to World Anvil's API documentation. This documentation is meant to serve as guide on how to use the API in order to access data on World Anvil according to the permissions granted to the owner of the authorization token supplied.

This API is working exclusively using JSON. All requests should be made using content-type application/json. All responses will be returned with application/json.

Endpoints
For the purposes of this documentation all endpoints are assumed to be prefixed by /api/aragorn under the worldanvil domain. For example to get a list of your worlds you will have to call


GET https://www.worldanvil.com/api/aragorn/world/{id} HTTP/1.1
        
GET, POST and PATCH endpoints request and respond with JSON.
It is suggested that if needed, you use Content-type: application/json.
POST and PATCH do not use form-data to receive content.

Setup & Authentication
Authentication
In order to make use of the API you will need to have two things.

An application key, this is only supplied to those creating their own applications. In order to get one please fill this form
A User Authentication token, a user can generate a User Authentication token from their User API Tokens page
Both of them should be supplied with each call to the api as header variables under the keys x-application-key and x-auth-token respectively

Warning
It is your responsibility that the tokens above are not exposed to the public. All communications to and from the server are encrypted but your application should make sure these are kept safe.
Call Headers Setup
Finally keep in mind that all calls should also include in their header Content type application/json and a User-Agent with the name, url and version of the app.


x-auth-token: 9QxWuGXFsLX85Mb29kCcfQqMm0h5IPWL6k2F1xQlDhP5KrvspPafapCX0ayMM9gBaqP1O0gY6KPLLrSkNaWpr6WQWvyPFHTEgHEPugzYJENz2LYZu3iyKxLS29PrLFif52MLMHgpaWICMddtx7DBiRFuWwPOzDjGxd9XDJWYIqWoim2X6f12wSdwhQvulJFoIMJPaOf9bSd1c7qcGyAcNayS7GRgJbU6vwQQQFwvODQdYMcFoPAP8vCuX
x-application-key: Tt8RbuX7KD65F6QSHmhWvZLT7VAfCbZqbyBT6vY6BhbwfH4R2Y3
Content-type: application/json
User-Agent: $app_name ( $url, $version )
                                
Problems with CORS?
Although it is suggested that you use the headers for authentication, the same tokens with the same names can also be used as parameters to your calls. This is only suggested if for some reason you have issues with CORS while trying to connect.


GET http://localhost:8080/app_dev.php/api/aragorn/user?x-application-key=USER_APPLICATION_KEY_HERE&x-auth-token=USER_AUTH_TOKEN_HERE HTTP/1.1
                                            
Bug Reporting
If you find a bug please come and talk to me on our Discord on the #development-discussion channel. I would like issues related with the API to be handled swiftly so I will be pushing those directly to the development board (no need to go through the bug-reporting process)

Backwards Compatibility
Just a note here but I wanted to make sure that you will never have issue with deprecations of calls, any new breaking updates will be creating a new version of the API.

If a version of the API is being deprecated you will receive at least 3 months notice.

In some cases while I still iron things out and establish some basis, things might change but not without ample warning and only if it's absolutely necessary

Grab your hammer and ... GO BUILD APPS!
I am so very excited to give the chance to some of the most creative people I know to use the resources of World Anvil in order to create amazing stuff!

If you are interested into creating an application that will be using the resources of the API come and talk to me on Discord (Dimitris) or twitter @dimitrisromeo. Of course, there will be a more streamlined and automated process in the near future but to begin with, I would like to get to know you and help you personally with all you might need.

Keep in mind but for the time being on Grandmasters, Sages and members of the Inner Sanctum can get access to Application keys. I am trying to keep things as constrained as possible while I am developing the first version of the API.

Article 
GET
Get the data of a single article. The article always includes the "content" and "content_parsed" values but it will only display any additional sections if a value is present.

Method	Endpoint	Headers
GET	article/{article.id}	Default
Parameters
Call parameters that can be used to order and paginate the results. Default values in bold.

Parameter	Values	Type
load_all_properties	true | false	boolean
load_all_properties

Use this parameter in order to display all properties including empty ones. This is a good way to understand the full structure of the object. It's recommended only when debugging or preparing your implementation.

Sample Result

{
	"id": "11a70435-f489-43ea-ae22-ec1cff3b7ee3",
	"title": "Farah Raj-Hamilton",
	"template": "person",
	"is_wip": false,
	"is_draft": false,
	"state": "public",
    "passcode": "private_passcoded_article"
	"wordcount": 204,
	"creation_date": {
		"date": "2020-03-06 18:51:32.000000",
		"timezone_type": 3,
		"timezone": "Europe/London"
	},
	"update_date": {
		"date": "2020-06-11 09:13:58.000000",
		"timezone_type": 3,
		"timezone": "Europe/London"
	},
	"publication_date": {
		"date": "2020-03-06 18:51:32.000000",
		"timezone_type": 3,
		"timezone": "Europe/London"
	},
	"notification_date": null,
	"tags": "",
	"url": "http://localhost:8080/app_dev.php/w/tequila-starrise/a/farah-raj-hamilton-person",
	"category": {
		"id": "e490b114-65bd-4882-bc90-212f4b0c7b52",
		"title": "The Adventures of Farah",
		"slug": "the-adventures-of-farah-category",
		"url": "http://localhost:8080/app_dev.php/w/tequila-starrise/c/the-adventures-of-farah-category"
	},
	"world": {
		"id": "1aab88e0-8423-461d-93fe-a09deb429837",
		"title": "Tequila Starrise",
		"slug": "tequila-starrise",
		"url": "http://localhost:8080/app_dev.php/w/tequila-starrise"
	},
	"author": {
		"id": "c2f5ae3b-6338-42aa-abb9-1f93098dcdab",
		"username": "Janet",
		"url": "http://localhost:8080/app_dev.php/author/Janet",
		"avatar": {
			"id": 664843,
			"url": "http://localhost:8080/uploads/images/34086e4041df3c15e444bc0efb850d83.PNG"
		}
	},
	"portrait": {
		"id": 897656,
		"url": "http://localhost:8080/uploads/images/71178a7a07ec8af6f82181d417c1a0e9.png"
	},
	"content": null,
	"content_parsed": "",
	"sections": {
		"excerpt": {
			"title": "",
			"position": "",
			"content": "Farah is a young pilot from the backwater lunar colony Alma, above the planet Celia Prime. 18 years old, she is filled with curiosity about the universe beyond her home, and a longing to answer the biggest questions of the universe.",
			"content_parsed": "Farah is a young pilot from the backwater lunar colony Alma, above the planet Celia Prime. 18 years old, she is filled with curiosity about the universe beyond her home, and a longing to answer the biggest questions of the universe."
		},
		"firstname": {
			"title": "",
			"position": "",
			"content": "Farah",
			"content_parsed": "Farah"
		},
		"lastname": {
			"title": "",
			"position": "",
			"content": "Raj-Hamilton",
			"content_parsed": "Raj-Hamilton"
		},
	},
	"relations": {
        "timeline": {
            "id": "35eccbb5-91cf-45ed-941f-017cb097de04",
            "title": "test for api",
            "position": "sidebar",
            "type": "timeline",
            "is_article": "false",
            "state": "public"
        },
		"vehicle": {
			"title": "",
			"position": "sidebar",
			"type": "singlular",
			"items": {
				"id": "f1bb4161-b95e-4bc2-b13e-068913d14bc5",
				"title": "Inigo Montoya",
				"type": "vehicle",
				"state": "public",
                "is_article": "true"
			}
		},
		"relatedorganizations": {
			"title": "",
			"position": "sidebar",
			"type": "collection",
			"items": [{
					"id": "06988d29-0358-4490-8f96-5ee9b6fe4ed1",
					"title": "Apis",
					"slug": "apis-article",
					"url": "http://localhost:8080/app_dev.php/w/tequila-starrise/a/apis-article",
					"type": "organization",
                    "is_article": "true"
				},
				{
					"id": "4a12b666-e45f-4fce-8c82-afff81d88425",
					"title": "Cult of Helios",
					"slug": "cult-of-helios-organization",
					"url": "http://localhost:8080/app_dev.php/w/tequila-starrise/a/cult-of-helios-organization",
					"type": "organization",
                    "is_article": "true"
				},
				{
					"id": "7ffeff2f-3503-497e-bca0-667b8c9b6c6c",
					"title": "Lockheed Martini",
					"slug": "lockheed-martini-organization",
					"url": "http://localhost:8080/app_dev.php/w/tequila-starrise/a/lockheed-martini-organization",
					"type": "organization",
                    "is_article": "true"
				}
			]
		}
	},
	"full_render": "\n                \n            \n        \n                             Farah  Raj-Hamilton \n                        \n                                                                                        Mental characteristics\n\n                            \n                \t\t\t\t    \n    \t\t\t    \n\t\t        \t\t            Education\n\t\t        \t\t    \n\t\t\t    Farah was educated by the standard Educational Matrix in her home colony, Alma. Knowing early on that she wanted to leave Alma and explore the galaxy, she focussed on System Operations, Vehicle Operation and Drivespace Navigation - the latter of which she proved to be unnervingly proficient in. Her high intelligence allowed her to learn quickly, and so she minored in Life Science. \n \nDanger is an everpresent reality on the colony of Alma, which is mostly still jungle and wilderness. Growing up, Farah was trained in survival and the basics of pistol usage and maintenance. Her parents insisted that she pursue social activites, so she joined the Dojo (run by Dr Pierre Vesser, a xenobiologist), where she learned considerably more about defensive martial arts than socialising with her fellow students.\n\t\n            \n                            \n                            \n                            \n                            \n                            \n                            \n                \n            \n                                        Personality Characteristics\n                        \n                        \n                        \n                        \n            \t\t\t\t    \n    \t\t\t    \n\t\t        \t\t            Virtues & Personality perks\n\t\t        \t\t    \n\t\t\t    Reflexes, Great Looks, Superior Intelligence\n\t\n            \n            \t\t\t\t    \n    \t\t\t    \n\t\t        \t\t            Vices & Personality flaws\n\t\t        \t\t    \n\t\t\t    Temper +2 (when concentration broken), Toxin Intelerance (+2 Con penalty against toxins and poisons)\n\t\n            \n                        \n                                                \n                        \n                        \n                        \n                        \n                        \n            \n                        \n            \n\n                        \n                        \n            \n        \n        \n                            \n                    Introduction to Tequila Starrise\n\nShow Table of Contents\n          \n            \n            \n          \n                \n            \n                                                \n                        \n                        \n                    \n                                \n                    \n                                                    Farah is a young pilot from the backwater lunar colony Alma, above the planet Celia Prime. 18 years old, she is filled with curiosity about the universe beyond her home, and a longing to answer the biggest questions of the universe.\n                                                \n\n                            \n                                                    \n                                                    View Character Profile\n                                                                    \n                \n\n            \n                        \n                \n                    \n                    \n\n                        \n                        \n\n                        \n\n\n                                                    \n        \n                            Currently Boarded Vehicle\n                    \n        \n                    \t   Inigo Montoya\n                    \n    \n\n                        \n                        \n                        \n                        \n                        \n                        \n                        \n                        \n                        \n\n\n                        \n                        \n                        \n                        \n                                                \n\n                        \n                        \n                        \n                        \n                            \n        \n                            Eyes\n                    \n        \n            Amber, almond shaped\n        \n    \n\n                            \n        \n                            Hair\n                    \n        \n            Dark brown, straight\n        \n    \n\n                            \n        \n                            Skin Tone\n                    \n        \n            Light brown\n        \n    \n\n                            \n        \n                            Height\n                    \n        \n            5'9\n        \n    \n\n                            \n        \n                            Weight\n                    \n        \n            65kg\n        \n    \n\n                        \n                        \n                        \n                                                                                                                                            \n\n            \n                                    Other Affiliations\n                            \n            \n                \n                                                                         Apis\n                                                                                                 Cult of Helios\n                                                                                                 Lockheed Martini\n                                                            \n                        \n                   \n    \n                        \n                        \n                        \n                        \n                                            \n                    \n                \n            \n            \n            \n        \n    \n\n    \n"
    }
    
POST
Create a new article

Method	Endpoint	Headers
POST	article	Default
Parameters
Parameter	Values	Default	Type	Description
world	World Id	REQUIRED	UUID	ID of the world the article is contained in.
title		REQUIRED	string (256)	Title of the article
template	Generic Article (article)
Character (person)
Conflict (militaryConflict)
Condition (condition)
Document (document)
Ethnicity (ethnicity)
Formation (formation)
Geographic location (location)
Generic article (article)
Item (item)
Language (language)
Law (law)
Location, Settlement (settlement)
Locations, Landmark (landmark)
Material (material)
Myth / Legend (myth)
Organization (organization)
Prose (prose)
Profession (profession)
Rank/Title (rank)
Spell (spell)
Species (species)
Technology (technology)
Tradition / Ritual (ritual)
Vehicle (vehicle)
REQUIRED	string	Template type
custom_article_template			UUID	ID of the Article's custom template (if any)
isDraft	0 | 1	1	bool	Is the article a draft
isWip	0 | 1	1	bool	Is the article still in progress
isAdultContent	0 | 1	0	bool	NSFW/18+ Flag for article
state	public | private	world.state	string	Is the article private or visible to everyone
category			UUID	The ID of the category the article is under
articleParent			UUID	The ID of the article this article is under. articleParent will override category if both are inputted.
parent			UUID	The ID of the article this article is a logical child of. Same template articles only, when applicable.
cover			Number	The ID of the image this article will use as cover for its page.
content			Text	The main content of the article
tags			Text	Comma separated list of the tags that are assigned to the article.
seeded			Text	Storyteller seeded content visible only to world owner and authors.
sidebarcontent			Text	Sidebar content appearing on top of the panel
sidepanelcontenttop			Text	Sidebar content appearing in the panel on the top of other contentl
sidepanelcontent			Text	Sidebar content appearing in the panel on the bottom of other contentl
sidebarcontentbottom			Text	Sidebar content appearing under the sidebar panel
footnotes			Text	Appears on the left hand side under the content
fullfooter			Text	Appears under both left ahd righthand sidebar covering the full width
authornotes			Text	Appear over the comments section
credits			Text	Appear under the title of the article, full width
scrapbook			Text	Hidden content visible only when the article is edited
excerpt			string (256)	Appears as a short description on article blocks and other locations
pronunciation			string (256)	Pronunciation of the article, appears on the side of the article's title
subheading			string (256)	Appears under the header of the article
icon			string(50)	RPGAwesome or FontAwesome CSS class for the icon of the article
position			Number	Ordering weight of the article within its category
userMetadata			JSON	Article JSON metadata array. Variables set in here can be used in the article as part of its template.
*			*	There are over 600+ Template specific properties that will not be addressed in detail at this point.
Sample Request

{
   "title":"Aramalia Cite",
   "world":"0ab48160-0f21-4d9e-b511-f1cccbaae316",
   "template":"settlement",
   "isDraft":1,
   "isWip":1,
   "category":"a344b182-8e20-46b2-8356-d6df2cf03794",
   "tags":"city,capital,trade",
   "seeded":"The hideout of the Great Evil Man",
   "sidebarcontent":"[img:12345]",
   "fullfooter":"[h2]Additional Information[/h2][block:123]",
   "credits":"Created by Dimitris, Edited by Janet",
   "footnotes":"Find more info...",
   "content":"The great city of Aramalia is the jewel of the ...",
   "excerpt":"The city of Aramalia and its secrets",
   "scrapbook": "TODO: Write about Great Evil Man",
   "pronunciation":"AraMAlia",
   "icon":"fas fa-city",
   "cover":2294556
}
UPDATE
Update (patch) the content of an article.

Method	Endpoint	Headers
PATCH	article/{id}	Default
Parameters
Non of the parameters are required.

Parameter	Values	Default	Type	Description
title			string (256)	Title of the article
isDraft	0 | 1	1	bool	Is the article a draft
isWip	0 | 1	1	bool	Is the article still in progress
isAdultContent	0 | 1	0	bool	NSFW/18+ Flag for article
state	public | private	world.state	string	Is the article private or visible to everyone
category			UUID	The ID of the category the article is under
articleParent			UUID	The ID of the article this article is under. articleParent will override category if both are inputted.
parent			UUID	The ID of the article this article is a logical child of. Same template articles only, when applicable.
cover			Number	The ID of the image this article will use as cover for its page.
content			Text	The main content of the article
tags			Text	Comma separated list of the tags that are assigned to the article.
seeded			Text	Storyteller seeded content visible only to world owner and authors.
sidebarcontent			Text	Sidebar content appearing on top of the panel
sidepanelcontenttop			Text	Sidebar content appearing in the panel on the top of other contentl
sidepanelcontent			Text	Sidebar content appearing in the panel on the bottom of other contentl
sidebarcontentbottom			Text	Sidebar content appearing under the sidebar panel
footnotes			Text	Appears on the left hand side under the content
fullfooter			Text	Appears under both left ahd righthand sidebar covering the full width
authornotes			Text	Appear over the comments section
credits			Text	Appear under the title of the article, full width
scrapbook			Text	Hidden content visible only when the article is edited
excerpt			string (256)	Appears as a short description on article blocks and other locations
pronunciation			string (256)	Pronunciation of the article, appears on the side of the article's title
subheading			string (256)	Appears under the header of the article
icon			string(50)	RPGAwesome or FontAwesome CSS class for the icon of the article
position			Number	Ordering weight of the article within its category
userMetadata			JSON	Article JSON metadata array. Variables set in here can be used in the article as part of its template.
*			*	There are over 600+ Template specific properties that will not be addressed in detail at this point.
Sample Request

{
   "title":"Aramalia Cite",
   "isDraft":0,
   "isWip":0,
   "content":"The great city of Aramalia is the jewel of the and some more content added here...",
   "scrapbook": "",
}
DELETE
Delete an article

Method	Endpoint	Headers
DELETE	article/{article.id}	Default
Block 
Block
Get the data of a single Statblock / Sheet

Method	Endpoint	Headers
GET	block/{block.id}	Default
Sample Result

{
    "id": 125,
    "name": "Sling",
    "template": {
        "id": 18,
        "title": "Item",
        "system": {
            "id": 1,
            "title": "Dungeons & Dragons 5e"
        }
    },
    "shared": true,
    "tags": null,
    "data": {
        "name": "Sling",
        "type": "Ranged Weapon",
        "attunement": "",
        "properties": "Ammunition",
        "armortype": "None",
        "ac": "",
        "strengthrequirement": "",
        "weapontype": "Simple",
        "damage": "1d4",
        "secondarydamage": "",
        "damagetype": "Bludgeoning",
        "range": "30/120 ft",
        "description": "",
        "rarity": "Common",
        "cost": "1 sp",
        "weight": "",
        "source": "DnD 5e SRD",
        "image": "",
        "tabledata": "",
        "templateId": "18"
    },
    "world": {
        "id": "036c02bb-38f9-4a61-9ebb-0f59bd933aeb",
        "title": "DnD 5E SRD & World Anvil Homebrew",
        "slug": "dnd-5e-srd--world-anvil-homebrew-worldanvil",
        "url": "http://localhost:8080/app_dev.php/w/dnd-5e-srd--world-anvil-homebrew-worldanvil"
    },
    "author": {
        "id": "88ed6bb8-37e0-4478-b2d9-196a73d94236",
        "username": "Padrone56",
        "url": "http://localhost:8080/app_dev.php/author/Padrone56",
        "avatar": {
            "id": 10892,
            "url": "http://localhost:8080/uploads/images/a65cf29c0f4cc8ce8103f415b49776e8.jpg"
        }
    }
}
                                    
Category 
Category
Get the data of a single Category

Method	Endpoint	Headers
GET	category/{category.id}	Default
Sample Result

{
    "id": "0561a109-7031-4f01-92ed-350aa7c40568",
    "title": "World Atlas",
    "state": "public",
    "views": null,
    "description": "The lands of this world. Mountains, Rivers, Valleys, Cities and Landmarks.",
    "excerpt": null,
    "icon": "fas fa-star",
    "position": 1000,
    "url": "http://localhost:8080/app_dev.php/w/testia-dimitris/c/world-atlas-category",
    "page_cover": {
        "id": 2294552,
        "url": "http://localhost:8080/uploads/images/e62f75af12c347ff948d322ae8d3857c.png"
    },
    "book_cover": {
        "id": 2294554,
        "url": "http://localhost:8080/uploads/maps/746c777e5349db89980637c331b699af.jpg"
    },
    "parent_category": {
        "id": "a344b182-8e20-46b2-8356-d6df2cf03794",
        "title": "World Encyclopedia",
        "slug": "world-encyclopedia-category",
        "url": "http://localhost:8080/app_dev.php/w/testia-dimitris/c/world-encyclopedia-category"
    },
    "world": {
        "id": "0ab48160-0f21-4d9e-b511-f1cccbaae316",
        "title": "Testia",
        "slug": "testia-dimitris",
        "url": "http://localhost:8080/app_dev.php/w/testia-dimitris"
    }
}
                                        
Image 
Image
Get the data of a single Image

Method	Endpoint	Headers
GET	image/{image.id}	Default
Sample Result

{
    "id": 123,
    "title": "seventomesbadge.png",
    "description": null,
    "tags": "#seven-tomes",
    "state": "public",
    "size": 60084,
    "width": 782,
    "height": 782,
    "extension": "png",
    "url": "http://localhost:8080/uploads/images/f25afae2fca6f06a7727231075329ff1.png",
    "world": {
        "id": "1d4bd15a-7b02-4324-8848-840cfe44c10d",
        "title": "Macalgra",
        "slug": "macalgra-xanthussmarduk",
        "url": "http://localhost:8080/app_dev.php/w/macalgra-xanthussmarduk"
    },
    "author": {
        "id": "c672c91d-207e-4dc0-b903-8015f2811920",
        "username": "XanthussMarduk",
        "url": "http://localhost:8080/app_dev.php/author/XanthussMarduk",
        "avatar": {
            "id": 178861,
            "url": "http://localhost:8080/uploads/images/201478a4f51b3dd610d88343c99f25dc.png"
        }
    }
}
                                        
Manuscript 
Manuscript
Get the data of a world

Method	Endpoint	Headers
GET	manuscript/{id}	Default
Sample Result

{
    "id": "956b982b-b6f5-4468-b81b-3a741c584755",
    "title": "The Book of Nodes II The return",
    "status: "ongoing",
    "slug": "0860357733-dimitris-the-book-of-nodes-ii-the-return",
    "description": "Thelma''s life [b]takes[/b] an exciting turn when she moves back to her hometown. \"\n",
    "description_parsed": "Thelma's life takes an exciting turn when she moves back to her hometown.\n",
    "likes": 12,
    "views": 107,
    "words": 10263,
    "world": {
        "id": "0b00e34e-7ef2-4443-876b-95787361a82c",
        "title": "Halloweenia",
        "slug": "halloweenia-dimitris",
        "url": "http://localhost:8080/app_dev.php/w/halloweenia-dimitris"
    },
    "cover": {
        "id": 1086575,
        "url": "http://localhost:8080/uploads/images/15d47f703a2d6bf629c9dbfe3eddb28a.jpg"
    },
    "author": {
        "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
        "username": "Dimitris",
        "url": "http://localhost:8080/app_dev.php/author/Dimitris"
    },
    "active_version": [
        {
            "id": "67a52d9f-3617-4ca3-9d2f-e829b4e7ca09",
            "title": "Draft 1",
            "state": "public"
        }
    ],
    "versions": [
        {
            "id": "67a52d9f-3617-4ca3-9d2f-e829b4e7ca09",
            "title": "Draft 1",
            "state": "public"
        }
    ]
}
                                        
Manuscript Version 
Manuscript Version
Get the data of a Manuscript's version

Method	Endpoint	Headers
GET	manuscript/version/{id}	Default
Sample Result

{
    "id": "67a52d9f-3617-4ca3-9d2f-e829b4e7ca09",
    "title": "Draft 1",
    "state": "public"
}
                                        
Manuscript Version (Export)
This method is a shortcut only available to the owners of the manuscript.
Quick Export of the parts directly under the manuscript root part.
Note Only parts up to 4 levels down will be exported. This should well cover an Act > Chapter > Scene structure
Note This does not include any other supporting folders.

Method	Endpoint	Headers
GET	manuscript/version/{id}/export	Default
Sample Result

{
    "manuscript": {
        "id": "956b982b-b6f5-4468-b81b-3a741c584755",
        "title": "The Book of Nodes II The return",
        "state": "public"
        "status: "completed",
    },
    "version": {
        "id": "67a52d9f-3617-4ca3-9d2f-e829b4e7ca09",
        "title": "Draft 1",
        "state": "public"
    },
    "parts": {
        "4b8a6f64-11fa-4c2c-a446-6e22499d959f": {
            "id": "4b8a6f64-11fa-4c2c-a446-6e22499d959f",
            "type": "text",
            "title": "Foreword",
            "content": "atlaskit this is a new version with words to count."
        },
        "9b59fad0-761e-426e-9dfa-ed0d3adab8e2": {
            "id": "9b59fad0-761e-426e-9dfa-ed0d3adab8e2",
            "type": "folder",
            "title": "Prologue",
            "content": null,
            "children": {
                "fcaf6195-f17f-415a-9599-4447f756cb1b": {
                    "id": "fcaf6195-f17f-415a-9599-4447f756cb1b",
                    "type": "folder",
                    "title": "Pro Prologue",
                    "content": null,
                    "children": {
                        "fb676097-6e66-4b99-a77d-a4efec6a2aa8": {
                            "id": "fb676097-6e66-4b99-a77d-a4efec6a2aa8",
                            "type": "text",
                            "title": "Pro Prologue Text",
                            "content": "This is the content"
                        }
                    }
                },
                "44cccdd7-63ba-435d-931c-67474f0923fa": {
                    "id": "44cccdd7-63ba-435d-931c-67474f0923fa",
                    "type": "text",
                    "title": null,
                    "content": "This is the world of the one egg that was a cat in a box of coffee. \n  dsad add dasda dasas dsadsadasd sad asdsa da asasdasdsa dsa asd sad asdasd as dsadsad dasdsadas asdasdasdas adsadasdas asdadsada asdasda asdasd asd dead asda sadasda as dasda asdas dasdas sadsadsad asdasdasdas dasdasda asdasdsada asdasdas adadasdas asdasdasd dsa dsadsa dead sadas sdadad sad asdas sadasdasd sd asdsad add adas das sd adasda asadasd  dasda"
                },
                "70c76b47-1804-47e6-b3de-55fecbc7d5d5": {
                    "id": "70c76b47-1804-47e6-b3de-55fecbc7d5d5",
                    "type": "image",
                    "title": "the truth",
                    "content": "My wove",
                    "image": {
                        "id": 1086584,
                        "url": "http://localhost:8080/uploads/maps/5ea0a7d58e42b388b0d0cba26513896f.jpg"
                    }
                },
...
                                        
Secret 
Secret
Get the data of a single Secret

Method	Endpoint	Headers
GET	secret/{secret.id}	Default
Sample Result

{
    "id": "4a16dc42-3320-421e-a142-5c7da2d591e0",
    "title": "The great chasm",
    "content": "content\r\n\r\n[h1]The truth[/h1]\r\nThe chasm is a massive illusion.",
    "content_parsed": "The truthThe chasm is a massive illusion"
    "state": "private",
    "tags": "",
    "author": {
        "id": "ba68d39e-7bd6-415b-9774-68c122e8d444",
        "username": "admin",
        "url": "http://localhost/author/admin",
        "author": {
            "avatar": {
                "id": 2294568,
                "url": "http://localhost/uploads/images/f7ba6fb25cb933cddf2b4333e206f9bc.jpg"
            }
        }
    },
    "subscribergroups": [
        {
            "id": "c6b6fffa-9b48-42ea-9a4a-1373e2332266",
            "title": "Player 1e"
        }
    ]
}
                                        
User 
Current User
Get the data of the currently Authenticated user

Method	Endpoint	Headers
GET	user	Default
User
Get the data of a user

Method	Endpoint	Headers
GET	user/{user.id}	Default
Sample Result

{
    "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
    "username": "Dimitris",
    "firstname": "Dimitris",
    "lastname": "Havlidis",
    "bio": "Incurable storyteller, builder of worlds, builder of applications for building worlds. Web Developer, Designer, Psychologist. Husband to a glorious wife. Humbled by those who supports his efforts. Oh and I really love chocolate and tangy lemon pies.",
    "deviantart": "lordceleborn",
    "youtube": "test",
    "twitch": null,
    "discord": null,
    "instagram": null,
    "kofi": "dimitris",
    "patreon": null,
    "twitter": "dimitrisromeo",
    "facebook": "dimitrishavlidis",
    "reddit": "iamromeo",
    "locale": "en",
    "membership": true,
    "membership_type": "special",
    "registration_date": {
        "date": "2017-09-06 00:00:00.000000",
        "timezone_type": 3,
        "timezone": "Europe/London"
    },
    "url": "http://localhost:8080/app_dev.php/author/Dimitris",
    "avatar": {
        "id": 4,
        "url": "http://localhost:8080/uploads/images/c554c7c3ca43671e2201b4fd7cd28008.jpeg"
    }
}
                                    
User Manuscripts
Get a list of all public manuscripts of a user. If the user is the authenticated user this list will also include private manuscripts.

Method	Endpoint	Headers
GET	user/{user.id}/manuscripts	Default
Sample Result

{
    "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
    "username": "Dimitris",
    "manuscripts": [
        {
            "id": "956b982b-b6f5-4468-b81b-3a741c584755",
            "state": "public",
            "name": "The Book of Nodes II",
            "slug": "0860357733-dimitris-the-book-of-nodes-ii-the-return"
        },
        {
            "id": "d57a8a31-a9e5-4806-b1fc-b01d12b6772f",
            "state": "private",
            "name": "The Harsh Truth",
            "slug": "9281334748-dimitris-the-harsh-truth"
        }
    ]
}
                                    
User Worlds
Get a list of all public worlds of a user. If the user is the authenticated user this list will also include private worlds.

Method	Endpoint	Headers
GET	user/{user.id}/worlds	Default
Sample Result

{
    "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
    "username": "Dimitris",
    "worlds": [
        {
            "id": "a455057d-1f12-4016-a00a-52d62229603f",
            "state": "public",
            "name": "Ambrosia"
        },
        {
            "id": "e0419f76-4623-4a3a-ab7f-aef938ed1fac",
            "state": "public",
            "name": "Azria"
        },
        {
            "id": "8a2ba444-6dd9-4627-884b-72702a33415d",
            "state": "private",
            "name": "Dissonance"
        },
        {
            "id": "f450b770-87df-4193-a93f-65d8af91e53c",
            "state": "private",
            "name": "Guide to Worldbuilding for Tabletop Roleplaying games"
        },
        {
            "id": "0b00e34e-7ef2-4443-876b-95787361a82c",
            "state": "public",
            "name": "Halloweenia"
        },
        {
            "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
            "state": "public",
            "name": "Hydria"
        },
        {
            "id": "b649619d-79b0-4fea-9910-34ef52036c04",
            "state": "public",
            "name": "Lyra"
        },
        {
            "id": "1aab88e0-8423-461d-93fe-a09deb429837",
            "state": "public",
            "name": "Tequila Starrise"
        }
    ]
}
                                    
World 
GET
Get the data of a world

Method	Endpoint	Headers
GET	world/{id}	Default
Sample Result

{
    "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
    "name": "Hydria",
    "locale": "en",
    "description": "[i][b]High Medieval, Age of Exploration meets hard science fiction in an unholy marriage of flying pirate ships, aliens and wondrous relics of unimaginable beauty and technology.[/b]\r\n[/i]\r\n\r\n\r\nIn everyday life, most inhabitants live in a world which resembled 1450 AD Earth. Think Leonardo Da Vinci, Copernicus, a strong church patronizing the arts,  Shakespearean Theatre and the ideals of Humanism in the backdrop of a an age of exploration of new lands, colonies and of course pirates. Now add to that, thousands of close-to-magic relics scattered all over the world, robots and artificial intelligence entities aliens, biogenetic experiments and cyborgs and you will get an idea of what you are getting yourself into ... oh and did I mention Dragons?",
    "description_parsed": "High Medieval, Age of Exploration meets hard science fiction in an unholy marriage of flying pirate ships, aliens and wondrous relics of unimaginable beauty and technology.\n\n \n \nIn everyday life, most inhabitants live in a world which resembled 1450 AD Earth. Think Leonardo Da Vinci, Copernicus, a strong church patronizing the arts, Shakespearean Theatre and the ideals of Humanism in the backdrop of a an age of exploration of new lands, colonies and of course pirates. Now add to that, thousands of close-to-magic relics scattered all over the world, robots and artificial intelligence entities aliens, biogenetic experiments and cyborgs and you will get an idea of what you are getting yourself into ... oh and did I mention Dragons?",
    "display_css": ".map-ae7a3c29-5398-4cdb-8cc4-4e9f2e3b4275 .legend {\n    background: #fdf7d3;\n    color: #84731f;\n}\n\n\n.widget-white-label-mark {\ndisplay:none;\n}",
    "theme": 13,
    "tags": "",
    "slug": "hydria",
    "url": "http://localhost:8080/app_dev.php/w/hydria",
    "cover": {
        "id": 32,
        "url": "http://localhost:8080/uploads/images/18a40bf3c020a6b0b9470acf3414ce77.png"
    },
    "custom_article_templates": [
        {
            "id": "01f073dd-f368-45b8-bcfb-0122b01ae60a",
            "name": "Spaceship"
        }
    ],
    "author": {
        "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
        "username": "Dimitris",
        "url": "http://localhost:8080/app_dev.php/author/Dimitris",
        "avatar": {
            "id": 4,
            "url": "http://localhost:8080/uploads/images/c554c7c3ca43671e2201b4fd7cd28008.jpeg"
        }
    }
}
                                    
World 
PATCH
Update data of a world

Method	Endpoint	Headers
PATCH	world/{id}	Default
Parameters
Non of the parameters are required.

Parameter	Values	Default	Type	Description
name			string (256)	Name of the world
state	public | private		string	Is the world private or visible to everyone
subtitle			string (256)	Sub title appearing under the name of the world
description			Text	The description of the world
copyright			Text	Copyright notice of the world, appears at the footer of most pages.
global_announcement			Text	Appears on the top of the sidebar of each article in the world
global_header			Text	Appears on the very top of all world pages
global_sidebar_footer			Text	Appears on the bottom of the sidebar of each article in the world
global_article_introduction			Text	Appears under each article's title
world_sidebar_content			Text	Appears on the top of the left clickable sidebar
display_css			Text	World custom CSS rules for the Presentation layer
display_panel_css			Text	World custom CSS rules for the Editing layer
tags			Text	Comma separated list of the tags that are assigned to the article.
Sample Request

{
    "name": "Testus Majoris",
    "description":"Welcome to Testus",
    "display_css": ".page {\nbackground: teal;\n}\n\n.article-content {\n    font-size: 1.2em;\n    line-height: 1.4em;\n    background: #ededde;\n}",
    "global_announcement": "Welcome World!"
}
World Articles
Get a list of articles under a world. Always returns 25 results

Method	Endpoint	Headers
GET	world/{id}/articles	Default
Parameters
Call parameters that can be used to order and paginate the results. Default values in bold.

Parameter	Values	Type
term	?string null	String
offset	?numeric 0	Integer
order_by	id | title | notification_date | creation_date	string
trajectory	ASC | DESC	string
Sample Result

{
    "world": {
        "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
        "title": "Hydria",
        "slug": "hydria",
        "url": "http://localhost:8080/app_dev.php/w/hydria"
    },
    "term": "Kingdom",
    "offset": "1",
    "limit": "2",
    "order_by": "creationDate",
    "trajectory": "DESC",
    "articles": [
        {
            "id": "327293bc-cef9-43e3-b3f0-2e2cf0493174",
            "title": "Coinage in the Six Kingdoms",
            "state": "public",
            "is_wip": true,
            "is_draft": false,
            "template_type": "item",
            "wordcount": 118,
            "views": 79,
            "likes": null,
            "excerpt": null,
            "tags": "",
            "adult_content": false,
            "last_update": null,
            "url": "http://localhost:8080/app_dev.php/w/hydria/a/coinage-in-the-six-kingdoms-article",
            "author": {
                "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
                "username": "Dimitris",
                "url": "http://localhost:8080/app_dev.php/author/Dimitris",
                "avatar": {
                    "id": 4,
                    "url": "http://localhost:8080/uploads/images/c554c7c3ca43671e2201b4fd7cd28008.jpeg"
                }
            },
            "world": {
                "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
                "title": "Hydria",
                "slug": "hydria",
                "url": "http://localhost:8080/app_dev.php/w/hydria"
            }
        },
        {
            "id": "a82305e8-0b72-4eb2-a880-3c2a1132827b",
            "title": "The Kingdoms of Man",
            "is_wip": true,
            "is_draft": false,
            "template_type": "article",
            "wordcount": 712,
            "views": 361,
            "likes": 7,
            "excerpt": null,
            "tags": "",
            "adult_content": false,
            "last_update": null,
            "url": "http://localhost:8080/app_dev.php/w/hydria/a/the-kingdoms-of-man-article",
            "author": {
                "id": "a5168b7c-ef11-4d6b-9b9b-28c0fbd81254",
                "username": "Dimitris",
                "url": "http://localhost:8080/app_dev.php/author/Dimitris",
                "avatar": {
                    "id": 4,
                    "url": "http://localhost:8080/uploads/images/c554c7c3ca43671e2201b4fd7cd28008.jpeg"
                }
            },
            "cover": {
                "id": 102354,
                "url": "http://localhost:8080/uploads/maps/96eee073929119855811a89de2530c15.jpg"
            },
            "category": {
                "id": "15dc1526-8a3f-4844-96b8-cc3fa0733cea",
                "title": "The Kingdoms",
                "slug": "the-kingdoms--of-hydria",
                "url": "http://localhost:8080/app_dev.php/w/hydria/c/the-kingdoms--of-hydria"
            },
            "world": {
                "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
                "title": "Hydria",
                "slug": "hydria",
                "url": "http://localhost:8080/app_dev.php/w/hydria"
            }
        }
    ]
}
                                        
World Categories
Get a list of categories under a world. Returns 50 results

Method	Endpoint	Headers
GET	world/{id}/categories	Default
Parameters
Call parameters that can be used to order and paginate the results. Default values in bold.

Parameter	Values	Type
term	?string null	String
offset	?numeric 0	Integer
order_by	name | creation_date	string
trajectory	ASC | DESC	string
World Blocks
Get a list of statblocks under a world. Always returns 50 results

Method	Endpoint	Headers
GET	world/{id}/blocks	Default
Parameters
Call parameters that can be used to order and paginate the results. Default values in bold

Parameter	Values	Type
offset	?numeric 0	Integer
order_by	id | title	string
trajectory	ASC | DESC	string
Sample Result

{
    "world": {
        "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
        "title": "Hydria",
        "slug": "hydria",
        "url": "http://localhost:8080/app_dev.php/w/hydria"
    },
    "offset": "1",
    "limit": 50,
    "blocks": [
        {
            "id": 364,
            "shared": true,
            "name": "Voice of the Maw",
            "tags": "spell, unique"
            "template": {
                "id": 19,
                "title": "Spell",
                "system": {
                    "id": 1,
                    "title": "Dungeons & Dragons 5e"
                }
            }
        },
        {
            "id": 360620,
            "shared": false,
            "name": "Sword of the Loom",
            "tags": "weapon"
            "template": {
                "id": 2999,
                "title": "Item (2020)",
                "system": {
                    "id": 1,
                    "title": "Dungeons & Dragons 5e"
                }
        }
    ]
}
                                
World Images
Get a list of images under a world. Always returns 50 results

Method	Endpoint	Headers
GET	world/{id}/images	Default
Parameters
Call parameters that can be used to order and paginate the results. Default values in bold

Parameter	Values	Type
offset	?numeric 0	Integer
order_by	id | title	string
trajectory	ASC | DESC	string
Sample Result

{
    "world": {
        "id": "7879cbac-406b-4a1a-865a-7efc9928614e",
        "title": "Hydria",
        "slug": "hydria",
        "url": "http://localhost:8080/app_dev.php/w/hydria"
    },
    "offset": "42",
    "limit": 50,
    "order_by": "id",
    "trajectory": "ASC",
    "images": [
        {
            "id": 125114,
            "title": "Lighthouse of Myrieth cover",
            "state": "public",
            "url": "http://localhost:8080/uploads/maps/966abd75d073a0d3bc8cd1150418eb34.JPG"
        },
        {
            "id": 125643,
            "title": "Welcome to Hydria cover",
            "state": "public",
            "url": "http://localhost:8080/uploads/images/b3d3764e23f8a1a799e2b5a3bc94f1ac.jpg"
        },
        {
            "id": 149812,
            "title": "Principality of Veleria cover",
            "state": "public",
            "url": "http://localhost:8080/uploads/images/1aba1924d10575f026bca667e7dd5d74.jpg"
        },
        {
            "id": 205189,
            "title": "science_fantasy_thinkers_society",
            "state": "public",
            "url": "http://localhost:8080/uploads/images/8ac36361e80fc31c2386889d4b1282dd.png"
        }
    ]
}
                                
World Secrets
Get a list of Secrets under a world. Always returns 50 results

Method	Endpoint	Headers
GET	world/{id}/secrets	Default
Parameters
Call parameters that can be used to order and paginate the results. Default values in bold

Parameter	Values	Type
offset	?numeric 0	Integer
order_by	id | title	string
trajectory	ASC | DESC	string
Changelog 
Feb 26, 2021
GET /world/{id}/secrets

GET /secret/{id} New Endpoint

Sept 16, 2021
POST, PATCH and DELETE methods for the Article endpoint

July 3, 2021
GET /world/{id)/categories New Endpoint

GET /category/{id} New Endpoint

Sep 24, 2020
Updates
GET /world/articles Added property "state" for articles.

Sep 16, 2020
Updates
GET /article/{id} Added property "passcode" for articles which are under a passcode check.

Aug 30, 2020
Updates
GET /manuscript/{id} Added property status (ongoing/completed) GET /user/{id}/manuscripts Added property status (ongoing/completed)

August 18, 2020
Updates
GET /article/{id} Added property displaying the css classes and the CSS code attached to the article

July 11, 2020
Updates
GET /worlds/{id}/articles Now returns draft articles as well GET /world/{id}/articles now also returns is_wip (Work in progress) and (is_draft) Draft/Published

July 6, 2020
Updates
GET /user/{id}/manuscripts New Endpoint

GET /user/{id}/images New Endpoint

GET /image/{id} New Endpoint

GET /manuscript/{id} New Endpoint

GET /manuscript/version/{id} New Endpoint

GET /manuscript/version/{id}/export New Endpoint

June 16, 2020
Updates
GET /world/{id}/articles Added "notification_date" and updated last_update to show the action last update date.

June 12, 2020
Updates
GET /article/{id} Added "relationship_type" what the type of entity the relation links to.

June 11, 2020
Updates
GET /article/{id} Added "Relations" node to

GET /article/{id} Redesigned "Sections" node to

GET /article/{id} Added Portrait and Flag nodes (for Character and Organization respectively)

GET /article/{id} Add "full_render" node that returns a fully rendered version of the article

GET /article/{id} Added parameter load_all_properties to help with debugging and implementations

June 6, 2020
The first deployment of the API Documentation

Updates
Decided to go with plularization of collection resources

Changes GET /world/{id}/block to /world/{id}/blocks
Changes GET /world/{id}/article to /world/{id}/articles
Bugfixes
GET Article changed content_parse ro content_parsed
Upcoming Updates 
The following endpoints are considered for future development. Please feel free to discuss and suggest on our discord!



POST /category HTTP/1.1
DELETE /category/{id} HTTP/1.1
PATCH /category/{id} HTTP/1.1

GET /notebook/{id} HTTP/1.1
POST /notebook HTTP/1.1
DELETE /notebook/{id} HTTP/1.1
PATCH /notebook/{id} HTTP/1.1

GET /notesection/{id} HTTP/1.1
POST /notesection HTTP/1.1
DELETE /notesection/{id} HTTP/1.1
PATCH /notesection/{id} HTTP/1.1

GET /note/{id} HTTP/1.1
POST /note HTTP/1.1
DELETE /note/{id} HTTP/1.1
PATCH /note/{id} HTTP/1.1

GET /map/{id} HTTP/1.1
GET /secret/{id} HTTP/1.1
GET /group/{id} HTTP/1.1
GET /hero/{id} HTTP/1.1
GET /campaign/{id} HTTP/1.1

GET /user/{id}/notebook HTTP/1.1
GET /world/{id}/event HTTP/1.1
GET /world/{id}/image HTTP/1.1
GET /world/{id}/campaign HTTP/1.1
GET /world/{id}/map HTTP/1.1
GET /world/{id}/secret HTTP/1.1
GET /world/{id}/groups HTTP/1.1

                                
Licence 
This API and all it contents cannot be used for any sort of commercial project without prior authorization by World Anvil. This is a perpetual licence meaning that anything created using the API falls under this licence as well.

Modification
We may modify the Terms or any portion to, for example, reflect changes to the law or changes to our APIs. You should look at the Terms regularly. We'll post notice of modifications to the Terms within the documentation of each applicable API, to this website. Changes will not apply retroactively and will become effective no sooner than 30 days after they are posted. But changes addressing new functions for an API or changes made for legal reasons will be effective immediately. If you do not agree to the modified Terms for an API, you should discontinue your use of that API. Your continued use of the API constitutes your acceptance of the modified Terms.

Removal of Access
We hold the right at any point to remove access without prior consent. This might be the case if the application is in any way violating World Anvil's terms of service or tries to circumvent feature locks to specific guild membership levels. This is not limited to the above.

WARRANTIES
EXCEPT AS EXPRESSLY SET OUT IN THE TERMS, NEITHER WORLD ANVIL NOR ITS SUPPLIERS OR DISTRIBUTORS MAKE ANY SPECIFIC PROMISES ABOUT THE APIS. FOR EXAMPLE, WE DON'T MAKE ANY COMMITMENTS ABOUT THE CONTENT ACCESSED THROUGH THE APIS, THE SPECIFIC FUNCTIONS OF THE APIS, OR THEIR RELIABILITY, AVAILABILITY, OR ABILITY TO MEET YOUR NEEDS. WE PROVIDE THE APIS "AS IS".

SOME JURISDICTIONS PROVIDE FOR CERTAIN WARRANTIES, LIKE THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. EXCEPT AS EXPRESSLY PROVIDED FOR IN THE TERMS, TO THE EXTENT PERMITTED BY LAW, WE EXCLUDE ALL WARRANTIES, GUARANTEES, CONDITIONS, REPRESENTATIONS, AND UNDERTAKINGS.

LIMITATION OF LIABILITY
WHEN PERMITTED BY LAW, WORLD ANVIL, WILL NOT BE RESPONSIBLE FOR LOST PROFITS, REVENUES, OR DATA; FINANCIAL LOSSES; OR INDIRECT, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES.

TO THE EXTENT PERMITTED BY LAW, THE TOTAL LIABILITY OF WORLD ANVIL, FOR ANY CLAIM UNDER THE TERMS, INCLUDING FOR ANY IMPLIED WARRANTIES, IS LIMITED TO THE AMOUNT YOU PAID US TO USE THE APPLICABLE APIS (OR, IF WE CHOOSE, TO SUPPLYING YOU THE APIS AGAIN) DURING THE SIX MONTHS PRIOR TO THE EVENT GIVING RISE TO THE LIABILITY.

IN ALL CASES, WORLD ANVIL, WILL NOT BE LIABLE FOR ANY EXPENSE, LOSS, OR DAMAGE THAT IS NOT REASONABLY FORESEEABLE.

Indemnification
Unless prohibited by applicable law, if you are a business, you will defend and indemnify WORLD ANVIL, and its affiliates, directors, officers, employees, and users, against all liabilities, damages, losses, costs, fees (including legal fees), and expenses relating to any allegation or third-party legal proceeding to the extent arising from:

your misuse or your end user's misuse of the APIs;
your violation or your end user's violation of the Terms; or
any content or data routed into or used with the APIs by you, those acting on your behalf, or your end users.

Welcome
Endpoints
Authentication
Bug Reporting
Backwards Compatibility
Grab your hammer
Entities
Article
Block
Category
Image
Manuscript
Manuscript Version
Secret
User
World
Changelog
Upcoming Updates
Licence
Designed with by Dimitris Havlidis for the creative community of World Anvil 