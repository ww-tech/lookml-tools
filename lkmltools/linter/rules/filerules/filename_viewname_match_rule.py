'''
    a filename viewname rule

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from lkmltools.linter.rule import Rule

class FilenameViewnameMatchRule(Rule):
    '''
        does filename match the view name?
    '''

    def run(self, json_data):
        '''does filename match the view name?

        Args:
            json_data (JSON): json_data of the whole lookml-parser ouput for a file

        Returns:
            (tuple): tuple containing:

                relevant (bool): is this rule relevant for this JSON chunk?

                passed (bool): did the rule pass?

        '''
        if not 'views' in json_data: #['files'][0]:
            return False, None
        view_name = json_data['views'][0]['name'] #['files'][0]['views'][0]['_view']
        filename = json_data['base_filename'].replace(".view.lkml","") #files'][0]['_file_name']
        return True, view_name == filename
