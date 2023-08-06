#coding=utf-8
# How to test it?
# easy_install nose
# cd test
# nosetests test_form.py --with-doctest
from __future__ import print_function, absolute_import, unicode_literals
import time, sys
sys.path.insert(0, '../uliweb/lib')

from uliweb.form import *
from uliweb.utils.test import BlankRequest
import datetime
from uliweb.utils._compat import u

def test_1():
    """
    >>> class F(Form):
    ...     title = StringField(label='Title', required=True, help_string='Title help string')
    ...     content = TextField(label='Content')
    >>> f = F()
    >>> print (f) # doctest: +REPORT_UDIFF
    <form action="" class="form-horizontal" method="POST">
    <div class="control-group" id="div_field_title">
        <label class="control-label" for="field_title">Title:<span class="field_required">*</span></label>
        <div class="controls">
        <input class="" id="field_title" name="title" type="text" value=""></input>
        <p class="help help-block">Title help string</p>
    </div>
    <BLANKLINE>
    </div>
    <BLANKLINE>
    <div class="control-group" id="div_field_content">
        <label class="control-label" for="field_content">Content:</label>
        <div class="controls">
        <textarea class="" cols id="field_content" name="content" rows="4"></textarea>
        <p class="help help-block"></p>
    </div>
    <BLANKLINE>
    </div>
    <BLANKLINE>
    <BLANKLINE>
    <div class="form-actions">
        <button class="btn btn-primary" name="submit" type="submit">Submit</button>
    </div>
    <BLANKLINE>
    </form>
    <BLANKLINE>
    >>> req = BlankRequest('/test?title=&content=')
    >>> f.validate(req.GET)
    False
    >>> req = BlankRequest('/test?title=Hello&content=')
    >>> f.validate(req.GET)
    True
    >>> req = BlankRequest('/test?title=Hello&content=aaaa')
    >>> f.validate(req.GET)
    True
    >>> f.title.data
    'Hello'
    >>> f.title.data = 'limodou'
    >>> print (f.title.html)
    <input class="" id="field_title" name="title" type="text" value="limodou"></input>
    >>> print (F.title.html())
    <input class="" id="field_title" name="title" type="text" value=""></input>
    """

def test_select():
    """
    >>> from uliweb.form.widgets import Select
    >>> a = u('男', 'utf8')
    >>> b = u('女', 'utf8')
    >>> s = Select([(a, a), (b, b)], value=a, multiple=True)
    >>> print (s)
    <select multiple size="10">
    <option selected value="男">男</option>
    <option value="女">女</option>
    </select>
    <BLANKLINE>
    """
    
def test_form_class():
    """
    >>> class TForm(Form):
    ...     pass
    >>> form = TForm(html_attrs={'_class':'well form-inline'})
    >>> print (form)
    <form action="" class="well form-inline" method="POST">
    <div class="form-actions">
        <button class="btn btn-primary" name="submit" type="submit">Submit</button>
    </div>
    <BLANKLINE>
    </form>
    <BLANKLINE>
    >>> form = TForm(form_class='well form-inline')
    >>> print (form)
    <form action="" class="form-horizontal" method="POST">
    <div class="form-actions">
        <button class="btn btn-primary" name="submit" type="submit">Submit</button>
    </div>
    <BLANKLINE>
    </form>
    <BLANKLINE>
    """
    
def test_string():
    """
    >>> a = StringField(name='title', label='Title', required=True, id='field_title')
    >>> print (a.html('Test'))
    <input class="" id="field_title" name="title" type="text" value="Test"></input>
    >>> print (a.get_label())
    <label for="field_title">Title:<span class="field_required">*</span></label>
    >>> a.validate('')
    (False, 'This field is required.')
    >>> a.validate('Hello')
    (True, 'Hello')
    >>> a.to_python('Hello')
    'Hello'
    >>> a = StringField(name='title', label='Title', required=True)
    >>> print (a.html(''))
    <input class="" name="title" type="text" value=""></input>
    >>> print (a.get_label())
    <label>Title:<span class="field_required">*</span></label>
    >>> a.idtype = 'name'
    >>> print (a.html(''))
    <input class="" id="field_title" name="title" type="text" value=""></input>
    >>> print (a.get_label())
    <label for="field_title">Title:<span class="field_required">*</span></label>
    >>> a = StringField(name='title', label='Title:', required=True, html_attrs={'class':'ffff'})
    >>> print (a.html(''))
    <input class="ffff" name="title" type="text" value=""></input>
    """

def test_unicode_field():
    """
    >>> a = UnicodeField(name='title', label='Title', required=True, id='field_title')
    >>> print (a.html('Test'))
    <input class="" id="field_title" name="title" type="text" value="Test"></input>
    >>> print (a.get_label())
    <label for="field_title">Title:<span class="field_required">*</span></label>
    >>> a.validate('')
    (False, 'This field is required.')
    >>> a.validate('Hello')
    (True, 'Hello')
    >>> a.to_python('Hello')
    'Hello'
    >>> a.to_python('中国')
    '\u4e2d\u56fd'
    """
    
def test_password_field():
    """
    >>> a = PasswordField(name='password', label='Password:', required=True, id='field_password')
    >>> print (a.html('Test'))
    <input class="" id="field_password" name="password" type="password" value="Test"></input>
    """

def test_hidden_field():
    """
    >>> a = HiddenField(name='id', id='field_id')
    >>> print (a.html('Test'))
    <input class="" id="field_id" name="id" type="hidden" value="Test"></input>
    """

def test_list_field():
    """
    >>> a = ListField(name='list', id='field_list')
    >>> print (a.html(['a', 'b']))
    <input class="" id="field_list" name="list" type="text" value="a, b"></input>
    >>> print (a.validate('a b'))
    (True, ['a', 'b'])
    >>> print (a.validate(''))
    (True, [])
    >>> a = ListField(name='list', id='field_list', delimeter=',')
    >>> print (a.validate('a,b,c'))
    (True, ['a', 'b', 'c'])
    >>> a = ListField(name='list', id='field_list', delimeter=',', datatype=int)
    >>> print (a.validate('1,b,c'))
    (False, "Can't convert '1,b,c' to ListField.")
    >>> print (a.validate('1,2,3'))
    (True, [1, 2, 3])
    """

def test_text_field():
    """
    >>> a = TextField(name='text', id='field_text')
    >>> print (a.html('Test'))
    <textarea class="" cols id="field_text" name="text" rows="4">Test</textarea>
    """

def test_textlines_field():
    """
    >>> a = TextLinesField(name='list', id='field_list')
    >>> print (a.html(['a', 'b']))
    <textarea class="" cols id="field_list" name="list" rows="4">a
    b</textarea>
    """

def test_bool_field():
    """
    >>> a = BooleanField(name='bool', id='field_bool')
    >>> print (a.html('Test'))
    <input checked class="checkbox" id="field_bool" name="bool" type="checkbox"></input>
    >>> print (a.validate('on'))
    (True, True)
    >>> print (a.validate(''))
    (True, False)
    >>> print (a.validate(None))
    (True, False)
    """
        
def test_int_field():
    """
    >>> a = IntField(name='int', id='field_int')
    >>> print (a.html('Test'))
    <input class="" id="field_int" name="int" type="number" value="Test"></input>
    >>> print (a.validate(''))
    (True, 0)
    >>> print (a.validate(None))
    (True, 0)
    >>> print (a.validate('aaaa'))
    (False, "Can't convert 'aaaa' to IntField.")
    >>> print (a.validate('122'))
    (True, 122)
    >>> a = BaseField(name='int', id='field_int', datatype=int)
    >>> print (a.html('Test'))
    <input class="" id="field_int" name="int" type="text" value="Test"></input>
    >>> print (a.validate('122'))
    (True, 122)
    """

def test_select_field():
    """
    >>> choices = [('a', 'AAA'), ('b', 'BBB')]
    >>> a = SelectField(name='select', id='field_select', default='a', choices=choices, validators=[TEST_IN(choices)])
    >>> print (a.html('a'))
    <select class="" id="field_select" name="select">
    <option selected value="a">AAA</option>
    <option value="b">BBB</option>
    </select>
    <BLANKLINE>
    >>> print (a.validate(''))
    (True, 'a')
    >>> print (a.validate('aaaaaaa'))
    (False, 'The value is not in choices.')
    >>> print (a.validate('b'))
    (True, 'b')
    >>> a = SelectField(name='select', id='field_select', choices=[(1, 'AAA'), (2, 'BBB')], datatype=int)
    >>> print (a.validate(''))
    (True, None)
    >>> print (a.validate('2'))
    (True, 2)
    """

def test_radioselect_field():
    """
    >>> choices = [('a', 'AAA'), ('b', 'BBB')]
    >>> a = RadioSelectField(name='select', id='field_select', default='a', choices=choices, validators=[TEST_IN(choices)])
    >>> print (a.html('a'))
    <label class=""><input checked id="field_select" name="select" type="radio" value="a"></input>AAA</label>
    <label class=""><input id="field_select" name="select" type="radio" value="b"></input>BBB</label>
    >>> print (a.validate(''))
    (True, 'a')
    >>> print (a.validate('aaaaaaa'))
    (False, 'The value is not in choices.')
    >>> print (a.validate('b'))
    (True, 'b')
    """

def test_file_field():
    """
    >>> a = FileField(name='file', id='field_file')
    >>> print (a.html('a'))
    <input class="" id="field_file" name="file" type="file"></input>
    """
    
def test_time_field():
    """
    >>> a = TimeField(name='time', id='field_time')
    >>> print (a.html(datetime.time(14, 30, 59)))
    <input class="field_time" id="field_time" name="time" type="text" value="14:30:59"></input>
    >>> print (a.validate('14:30:59'))
    (True, datetime.time(14, 30, 59))
    >>> print (a.validate('14:30'))
    (True, datetime.time(14, 30))
    >>> print (a.validate(''))
    (True, None)
    >>> a = TimeField(name='time', id='field_time', default='now')
    """
    
def test_date_field():
    """
    >>> a = DateField(name='date', id='field_date')
    >>> print (a.html(datetime.date(2009, 1, 1)))
    <input class="field_date" id="field_date" name="date" type="text" value="2009-01-01"></input>
    >>> print (a.validate('2009-01-01'))
    (True, datetime.date(2009, 1, 1))
    >>> print (a.validate('2009/01/01'))
    (True, datetime.date(2009, 1, 1))
    >>> a = DateField(name='date', id='field_date', default='now')
    """
    
def test_datetime_field():
    """
    >>> a = DateTimeField(name='datetime', id='field_datetime')
    >>> print (a.html(datetime.datetime(2009, 9, 25, 14, 30, 59)))
    <input class="field_datetime" id="field_datetime" name="datetime" type="text" value="2009-09-25 14:30:59"></input>
    >>> print (a.validate('2009-09-25 14:30:59'))
    (True, datetime.datetime(2009, 9, 25, 14, 30, 59))
    >>> print (a.validate('2009-09-25 14:30'))
    (True, datetime.datetime(2009, 9, 25, 14, 30))
    >>> print (a.validate(''))
    (True, None)
    """

def test_form():
    """
    >>> class F(Form):
    ...     title = StringField(label='Title:')
    >>> form = F()
    >>> print (form.form_begin)
    <form action="" class="" method="POST">
    >>> class F(Form):
    ...     title = StringField(label='Title:')
    ...     file = FileField()
    >>> form = F(action='post')
    >>> print (form.form_begin)
    <form action="post" class="" enctype="multipart/form-data" method="POST">
    >>> print (form.form_end)
    </form>
    <BLANKLINE>
    """
    
def test_build():
    """
    >>> class F(Form):
    ...     title = StringField(label='Title:')
    >>> form = F()
    >>> build = form.build
    >>> print (build.pre_html)
    <BLANKLINE>
    >>> print (build.begin)
    <form action="" class="form-horizontal" method="POST">
    >>> print (build.body) #doctest: +REPORT_UDIFF
    <div class="control-group" id="div_field_title">
        <label class="control-label" for="field_title">Title::</label>
        <div class="controls">
        <input class="" id="field_title" name="title" type="text" value=""></input>
        <p class="help help-block"></p>
    </div>
    <BLANKLINE>
    </div>
    <BLANKLINE>
    <BLANKLINE>
    """
    
def test_form_hidden_field():
    """
    >>> class F(Form):
    ...     layout_class = BootstrapTableLayout
    ...
    ...     title = StringField(label='Title', required=True, help_string='Title help string')
    ...     content = HiddenField(label='Content')
    >>> f = F()
    >>> print (f) #doctest: +REPORT_UDIFF
    <form action="" class="form-horizontal" method="POST">
    <input class="" id="field_content" name="content" type="hidden" value=""></input>
    <table class="table table-layout width100"><tbody>
    <tr>
        <td colspan="1" valign="top" width="100%">
            <div class="control-group" id="div_field_title">
                <label class="control-label" for="field_title">Title:<span class="field_required">*</span></label>
                <div class="controls">
        <input class="" id="field_title" name="title" type="text" value=""></input>
        <div class="help help-block">
    Title help string
    </div>
    <BLANKLINE>
    </div>
    <BLANKLINE>
            </div>
        </td>
    </tr>
    <BLANKLINE>
    <tr>
    </tr>
    <BLANKLINE>
    </tbody></table>
    <BLANKLINE>
    <div class="form-actions">
        <button class="btn btn-primary" name="submit" type="submit">Submit</button>
    </div>
    <BLANKLINE>
    </form>
    <BLANKLINE>
    """
    
#if __name__ == '__main__':
#    from uliweb.utils import date
#    
#    class TForm(Form):
#        layout_class = BootstrapTableLayout
#        
#        title = StringField(label='Title', required=True, help_string='Title help string')
#        content = HiddenField(label='Content')
#        
#    form = TForm()
#    print form
