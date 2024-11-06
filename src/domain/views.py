from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "domain/index.html"

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        found, start, end, probable = self.parse_text(message, 'gmailcom')

        params = {
            'origin_message': message,
            'message_element': '',
            'resolution': '',
            'found': int(found),
            'probable': int(probable)
        }

        if found:
            if probable:
                params['resolution'] = 'can contain'
            else:
                params['resolution'] = 'contains'

            params['message_element'] = message[start:end]

        context = self.get_context_data(**kwargs)
        context.update(params)
        return self.render_to_response(context)

    def parse_text(self, text: str, domain: str, probable=False):
        sequence = [elem.lower() for elem in domain if elem.isalpha()]
        start_index = sequence_index = 0
        sequence_last_index = len(sequence) - 1
        in_sequence = False

        text = text.lower()
        text = text.replace('dot', '...').replace('at', '..').replace('0', 'o')

        for text_index, symbol in enumerate(text):
            if symbol.isalpha():
                if not in_sequence and symbol == sequence[sequence_index]:
                    in_sequence = True
                    start_index = text_index
                    continue

                if in_sequence and symbol == sequence[sequence_index]:
                    continue

                if in_sequence and symbol == sequence[sequence_index + 1]:
                    if sequence_index + 1 == sequence_last_index:
                        offset = 1
                        next_index = text_index + 1
                        try:
                            while text[next_index] == sequence[sequence_last_index]:
                                offset += 1
                                next_index += 1
                        except IndexError:
                            pass

                        try:
                            probable = text[next_index].isalpha()
                        except IndexError:
                            pass

                        return True, start_index, text_index + offset, probable

                    sequence_index += 1
                    continue

                if in_sequence:
                    in_sequence = False
                    start_index = 0
                    sequence_index = 0

        return False, 0, 0, probable