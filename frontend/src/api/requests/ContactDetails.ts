export interface ContactDetails {
    name: string;
    id: number;
}

export interface ContactDetailsById {
    [id: number]: ContactDetails;
}


export function getContactDetailsOfAllContacts(): [ContactDetails[], ContactDetailsById] {
    //will make http request using axios to get contact details, values will be hardcoded for now
    const contactDetailsList: ContactDetails[] = [
        {
        name: "John Doe",
        id: 0
        },
        {
        name: "Mary Jane",
        id: 1
        }
    ];

    const contactDetailsById: ContactDetailsById = {
        0: contactDetailsList[0],
        1: contactDetailsList[1]
    };

    return [contactDetailsList, contactDetailsById] ;
}

export function getContactDetailsOfOpenChats(allContacts: ContactDetails[]): ContactDetails[] {
    //will make http request using axios to get contact details, values will be hardcoded for now
    const contactDetailsOfOpenChats: ContactDetails[] = allContacts; //TODO: this line should go through all contacts list and make a new list of only the ones with open chats. It also should be sorted from most recent conversation to least recent conversation.
    return contactDetailsOfOpenChats;
}


 