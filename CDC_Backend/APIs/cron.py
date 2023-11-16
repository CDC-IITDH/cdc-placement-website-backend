from .models import *
from .utils import *
import shutil
import logging
import traceback

logger=logging.getLogger('db')
def clean_up_tests():
    # Delete all the test internships and placements created
    try:
        internships= Internship.objects.filter(company_name="test company",email="notifications@cdc-iitdh.tech")
        hits_internship=len(internships)
        for internship in internships:
            #count number of file
            files = os.listdir(STORAGE_DESTINATION_COMPANY_ATTACHMENTS+internship.id)
            if len(files) == 4:
                print("working fine")
            else:
                print("not working fine")
                logger.error("files submitted in inf are not getting stored for test case"+internship.description)

            #remove folder from the server
            print("removing folder ",STORAGE_DESTINATION_COMPANY_ATTACHMENTS+internship.id)
            shutil.rmtree(STORAGE_DESTINATION_COMPANY_ATTACHMENTS+internship.id)
            
            
            internship.delete()
        
        placements= Placement.objects.filter(company_name="test company",email="notifications@cdc-iitdh.tech")
        hits_placement=len(placements)
        for placement in placements:
            #count number of file
            files = os.listdir(STORAGE_DESTINATION_COMPANY_ATTACHMENTS+placement.id)
            if len(files) == 4:
                print("working fine")
            else:
                print("not working fine")
                logger.error("files submitted in inf are not getting stored for test case"+placement.description)

            #remove folder from the server
            print("removing folder ",STORAGE_DESTINATION_COMPANY_ATTACHMENTS+internship.id)
            shutil.rmtree(STORAGE_DESTINATION_COMPANY_ATTACHMENTS+placement.id)
            
            
            placement.delete()
        
        if hits_internship >= 6:
            print("all hits are working fine")
        else:
            print("some hits are not working fine")
            logger.error("some test hits are not working fine for internship")
        
        if hits_placement >= 6:
            print("all hits are working fine")
        else:
            print("some hits are not working fine")
            logger.error("some test hits are not working fine for placement")

    except :
        logger.error("error in clean up function")
        logger.error(traceback.format_exc())

    