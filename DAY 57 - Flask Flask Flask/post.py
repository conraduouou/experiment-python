class Post:
    def __init__(self, params):
        """Initializes Post class that contains id, title, subtitle, and body of post."""
        self.id = int(params['id'])
        self.body = params['body']
        self.title = params['title']
        self.subtitle = params['subtitle']
    pass