'''
@author: Santirrium
'''

class TwUser(object):

    def __init__(self, twitter_account, name, screen_name, location, url, protected, followers_count, friends_count, listed_count, favourites_count, statuses_count, created_at, 
                 utc_offset, profile_background_color, profile_background_image_url, profile_background_image_url_https, profile_background_tile, profile_banner_url,
                 profile_image_url, profile_image_url_https, profile_link_color, profile_sidebar_border_color, profile_sidebar_fill_color, profile_text_color,
                 profile_use_background_image, default_profile, default_profile_image, withheld_in_countries, withheld_scope, description, crit_date, 
                 crit_rt, crit_default_account, crit_location, crit_ratio_followers, crit_screen_name):
        '''
        Constructor
        '''
        self.twitter_account                    = twitter_account
        self.name                               = name                                 
        self.screen_name                        = screen_name                       
        self.location                           = location                          
        self.url                                = url                               
        self.protected                          = protected                         
        self.followers_count                    = followers_count                   
        self.friends_count                      = friends_count                     
        self.listed_count                       = listed_count                      
        self.favourites_count                   = favourites_count                  
        self.statuses_count                     = statuses_count                    
        self.created_at                         = created_at                        
        self.utc_offset                         = utc_offset                        
        self.profile_background_color           = profile_background_color          
        self.profile_background_image_url       = profile_background_image_url      
        self.profile_background_image_url_https = profile_background_image_url_https
        self.profile_background_tile            = profile_background_tile           
        self.profile_banner_url                 = profile_banner_url                
        self.profile_image_url                  = profile_image_url                 
        self.profile_image_url_https            = profile_image_url_https           
        self.profile_link_color                 = profile_link_color                
        self.profile_sidebar_border_color       = profile_sidebar_border_color      
        self.profile_sidebar_fill_color         = profile_sidebar_fill_color        
        self.profile_text_color                 = profile_text_color                
        self.profile_use_background_image       = profile_use_background_image      
        self.default_profile                    = default_profile                   
        self.default_profile_image              = default_profile_image             
        self.withheld_in_countries              = withheld_in_countries             
        self.withheld_scope                     = withheld_scope                    
        self.description                        = description
        self.crit_date                          = crit_date
        self.crit_rt                            = crit_rt
        self.crit_default_account               = crit_default_account
        self.crit_location                      = crit_location
        self.crit_ratio_followers               = crit_ratio_followers
        self.crit_screen_name                   = crit_screen_name
        
        
    def ToDbJson(self):
        return {
            'twitter_account'                     :  self.twitter_account                    ,
            'name'                                :  self.name                               ,
            'screen_name'                         :  self.screen_name                        ,
            'location'                            :  self.location                           ,
            'url'                                 :  self.url                                ,
            'protected'                           :  self.protected                          ,
            'followers_count'                     :  self.followers_count                    ,
            'friends_count'                       :  self.friends_count                      ,
            'listed_count'                        :  self.listed_count                       ,
            'favourites_count'                    :  self.favourites_count                   ,
            'statuses_count'                      :  self.statuses_count                     ,
            'created_at'                          :  self.created_at                         ,
            'utc_offset'                          :  self.utc_offset                         ,
            'profile_background_color'            :  self.profile_background_color           ,
            'profile_background_image_url'        :  self.profile_background_image_url       ,
            'profile_background_image_url_https'  :  self.profile_background_image_url_https ,
            'profile_background_tile'             :  self.profile_background_tile            ,
            'profile_banner_url'                  :  self.profile_banner_url                 ,
            'profile_image_url'                   :  self.profile_image_url                  ,
            'profile_image_url_https'             :  self.profile_image_url_https            ,
            'profile_link_color'                  :  self.profile_link_color                 ,
            'profile_sidebar_border_color'        :  self.profile_sidebar_border_color       ,
            'profile_sidebar_fill_color'          :  self.profile_sidebar_fill_color         ,
            'profile_text_color'                  :  self.profile_text_color                 ,
            'profile_use_background_image'        :  self.profile_use_background_image       ,
            'default_profile'                     :  self.default_profile                    ,
            'default_profile_image'               :  self.default_profile_image              ,
            'withheld_in_countries'               :  self.withheld_in_countries              ,
            'withheld_scope'                      :  self.withheld_scope                     ,
            'description'                         :  self.description                        ,
            'crit_date'                           :  self.crit_date                          ,
            'crit_rt'                             :  self.crit_rt                            ,
            'crit_default_account'                :  self.crit_default_account               ,
            'crit_location'                       :  self.crit_location                      ,
            'crit_ratio_followers'                :  self.crit_ratio_followers               ,
            'crit_screen_name'                    :  self.crit_screen_name                        
        }