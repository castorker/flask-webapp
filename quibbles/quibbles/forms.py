from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Regexp


class QuibbleForm(Form):
    text = StringField('Text:', validators=[DataRequired()])
    category = StringField('Category:', validators=[DataRequired()])
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message="Tags can only contain letters and numbers")])

    def validate(self):
        if not Form.validate(self):
            return False

        if not self.text.data:
            self.text.data = self.text.data

        if not self.category.data:
            self.category.data = self.category.data

        # filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True
