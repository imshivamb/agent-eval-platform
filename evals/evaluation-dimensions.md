# Evaluation Dimensions

Evaluating an AI agent requires more than determining whether it produced a response. A reliable evaluation framework should measure multiple aspects of an agent's performance, ensuring that the evaluation is objective, repeatable, and consistent across different scenarios and versions of the agent.

To achieve this, the framework defines a set of core evaluation dimensions. Each dimension measures a specific aspect of agent quality, such as its ability to satisfy user requirements, produce accurate information, generate high-quality plans, personalize responses, and adapt to changing constraints. Together, these dimensions provide a comprehensive view of an agent's overall performance while allowing each aspect to be evaluated independently.


## 1. Constraint Satisfaction

Constraint Satisfaction measures how well an AI agent fulfills the explicit requirements provided by the user. These requirements define the expected outcome of the task and form the primary criteria against which the agent is evaluated.

Examples of explicit constraints include budget limits, travel dates, trip duration, destinations, dietary restrictions, accessibility requirements, and other mandatory user preferences. An agent should satisfy these constraints as accurately as possible while generating its response.

Constraint Satisfaction focuses only on whether the user's stated requirements have been met. It does not evaluate the overall quality, creativity, or optimization of the solution, which are measured separately by other evaluation dimensions.

## 2. Planning Quality

Planning Quality measures how effectively an AI agent organizes and optimizes a solution while satisfying the user's requirements. A high-quality plan should be practical, realistic, and efficient rather than simply meeting the minimum set of constraints.

For a travel-planning agent, planning quality includes factors such as minimizing unnecessary travel, reducing frequent accommodation changes, grouping nearby attractions together, creating realistic daily schedules, and maintaining an appropriate balance between activities and rest. These characteristics improve the overall user experience without changing the user's original requirements.

Planning Quality evaluates how well the solution has been designed, rather than whether the required constraints have been met. Two itineraries may satisfy the same user requirements, but the itinerary with better organization, efficiency, and practicality should receive a higher planning quality score.


## 3. Information Accuracy

Information Accuracy measures how closely the information provided by an AI agent reflects real-world facts. A high-quality response should contain information that is current, reliable, and factually correct, allowing users to trust the recommendations provided by the agent.

For a travel-planning agent, this includes the accuracy of hotel prices, transportation costs, travel durations, attraction availability, opening hours, booking information, and other factual details that influence the user's decisions. Whenever possible, factual claims should be verifiable using trusted and up-to-date sources.

The purpose of this dimension is to evaluate the reliability of the information presented to the user, regardless of how the agent obtained it. Information Accuracy focuses on whether the output reflects reality, ensuring that users can confidently rely on the generated plan in real-world situations.

## 4. Personalization

Personalization measures how well an AI agent tailors its response to the individual user's preferences, interests, and requirements. A high-quality response should feel intentionally designed for the specific user rather than being a generic solution that could be given to anyone.

For a travel-planning agent, personalization includes adapting recommendations based on interests, travel style, budget, pace, accommodation preferences, dietary requirements, and other user-specific context. These preferences should meaningfully influence the decisions made throughout the itinerary rather than simply being acknowledged.

The purpose of this dimension is to evaluate whether the agent demonstrates an understanding of the user's unique context and produces recommendations that are personally relevant, resulting in a more useful and engaging experience.

## 5. Adaptability

Adaptability measures how effectively an AI agent incorporates new information, changing requirements, or unexpected events while maintaining the quality and consistency of its solution. Rather than rebuilding a solution from scratch, a well-designed agent should intelligently revise only the affected parts while preserving decisions that remain valid.

For a travel-planning agent, adaptability includes responding to changes such as budget adjustments, modified travel dates, destination changes, transportation disruptions, or evolving user preferences. The updated itinerary should continue to satisfy the user's requirements while minimizing unnecessary changes and maintaining an enjoyable overall experience.

The purpose of this dimension is to evaluate an agent's ability to respond to change in a practical and efficient manner. A highly adaptable agent should treat planning as an iterative process, continuously refining its solution as new information becomes available.