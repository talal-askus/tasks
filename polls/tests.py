from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        q= Question(pub_date=time)
        self.assertIs(q.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time=timezone.now()- datetime.timedelta(days=1, seconds=1)
        q= Question(pub_date=time)
        self.assertIs(q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):  
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        q = Question(pub_date=time)
        self.assertIs(q.was_published_recently(), True)

def create_question(question_text,days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


def create_choice(question, choice_text, votes=0):
    return Choice.objects.create(question=question, choice_text=choice_text, votes=votes)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")  
        self.assertQuerySetEqual(response.context["latest_question_list"],[])


    def test_past_question(self):
        q = create_question(question_text="Past Question ",days=-30)

        r = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            r.context["latest_question_list"],[q]
        )

    def test_future_question(self):
        create_question(question_text="Future Question",days=30)
        r = self.client.get(reverse("polls:index"))
        self.assertContains(r,"No polls are available")  
        self.assertQuerySetEqual(r.context["latest_question_list"],[])


    def test_future_question_and_past_question(self):
        
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )


    def test_two_past_questions(self):
        q1= create_question(question_text="Past Question 1", days=-30)
        q2= create_question(question_text="Past Question 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [q2, q1],
        )        

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        q = create_question(question_text="Future question", days = 5)
        url = reverse("polls:detail", args=(q.id))
        r= self.client.get(url)
        self.assertEqual(r.status_code,404)

    def test_past_questions(self):
        q=create_question(question_text="Past Questions", days=-5)
        url = reverse("polls:details",args=(q.id))

        r=self.client.get(url)
        self.assertContains(r,q.question_text)

    def test_past_question(self):  
        question = create_question(question_text="Past Question", days=-5)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)



