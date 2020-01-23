#
# https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
#
from app.handlers import PublishLatestGradesHandler

publisher = PublishLatestGradesHandler()


def handler(event, context):
    """
    https://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html
    """

    publisher.handle(event, context)

    return {}