"""WorkTimeSaver
Project was created for flextime employees to make easier daily logging of time spend at work. With this software each
employee is able to keep information on his own computer and confront it with paper lists used in company. Goals for
this project were to provide:
- easy for any kind of user way to store information and do corrections in case of mistakes
- summary after each month
    - number of days at work
    - sum of hours with deducted unpaid food break when work day is longer than set number of hours
    - salary before and after tax (with higher tax for overtime after set number of hours)
    - additional feature: salary exchanged to foreign currency


License:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from WorkTimeSaver.gui import Gui
from sys import platform


def main():
    """Sets GUI width according to used platform and runs it"""

    width = '390' if platform == 'win32' else '450'
    Gui('Work Time Saver', f'{width}x150').mainloop()


if __name__ == '__main__': main()
