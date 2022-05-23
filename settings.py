from database import DBManager
import models as md

class Settings:

    def settings_exist():
        data = DBManager.get_row(obj=md.Settings, id=1)
        if data[0] == None:
            print('creating default settings for first run of system')
            settings = md.Settings()
            DBManager.add_row(settings)
            data = DBManager.get_row(obj=md.Settings, id=1)
        return data[0]

    config = settings_exist()
    """
    id = Column(Integer, primary_key=True)
    localizer = Column(Boolean, default=False)
    pdf = Column(Boolean, default=True)
    csv = Column(Boolean, default=True)
    pic_format = Column(Boolean, default=True)
    v3d = Column(Boolean, default=False)
    results = Column(String, default='binary')

    """

    def mod(localizer, pdf, csv, pic_format, v3d, res):
        s = md.Settings(localizer, pdf, csv, pic_format, v3d, res)
        DBManager.mod_row(obj=s, id=1)
        data = DBManager.get_row(obj=md.Settings, id=1)
        Settings.config = data[0]
        
            
            

