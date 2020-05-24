from .models import Question, Answer, VoteQuestion, VoteAnswer
from django.db import transaction
from django.shortcuts import get_object_or_404


def vote(entity_id, entity_type, person, value):
    try:
        if entity_type == "question":
            entity = get_object_or_404(Question, id=entity_id)
            # if entity in person.questions:
            #     return None
            vote_obj = VoteQuestion.objects.get_or_create(author_id=person.id, entity_id=entity_id)[0]
        else:
            entity = get_object_or_404(Answer, id=entity_id)
            # if entity in person.answers:
            #     return None
            vote_obj = VoteAnswer.objects.get_or_create(author_id=person.id, entity_id=entity_id)[0]
    except Exception as e:
        print(e)

    with transaction.atomic():
        new_value = 0 if value == vote_obj.value else value
        entity.update_rating(new_value - vote_obj.value)
        vote_obj.value = new_value
        vote_obj.save()