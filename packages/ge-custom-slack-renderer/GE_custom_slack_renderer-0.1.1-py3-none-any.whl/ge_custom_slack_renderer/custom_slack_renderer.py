from great_expectations.core.id_dict import BatchKwargs
from great_expectations.render.renderer.renderer import Renderer

class BriefSlackRenderer(Renderer):
    def __init__(self):
        super().__init__()

    def render(self, validation_result=None, data_docs_pages=None):
        default_text = (
            "No validation occurred. Please ensure you passed a validation_result."
        )
        status = ":x:"

        title_block = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": default_text,},
        }

        query = {
            "blocks": [title_block],
            # this abbreviated root level "text" will show up in the notification and not the message
            "text": default_text,
        }

        if validation_result:
            expectation_suite_name = validation_result.meta.get(
                "expectation_suite_name", "__no_expectation_suite_name__"
            )

            n_checks_succeeded = validation_result.statistics["successful_expectations"]
            n_checks = validation_result.statistics["evaluated_expectations"]
            run_id = validation_result.meta.get("run_id", "__no_run_id__")
            batch_id = BatchKwargs(
                validation_result.meta.get("batch_kwargs", {})
            ).to_id()
            check_details_text = "(*{}/{}* expectations were met)".format(
                n_checks_succeeded, n_checks
            )

            if validation_result.success:
                status = ":heavy_check_mark:"

            summary_text = """`{}` {} {}""".format(
                expectation_suite_name, status, check_details_text,
            )
            query["blocks"][0]["text"]["text"] = summary_text
            # this abbreviated root level "text" will show up in the notification and not the message
            query["text"] = "{}: {}".format(expectation_suite_name, status)

        custom_blocks = self._custom_blocks(evr=validation_result)
        if custom_blocks:
            query["blocks"].append(custom_blocks)

        divider_block = {"type": "divider"}
        query["blocks"].append(divider_block)
        return query

    def _custom_blocks(self, evr):
        return None
